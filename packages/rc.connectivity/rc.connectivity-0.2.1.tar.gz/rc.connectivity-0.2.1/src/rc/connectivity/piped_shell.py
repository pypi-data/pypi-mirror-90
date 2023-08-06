
__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


import os
import time
import errno
import select
import signal

import multiprocessing as mp

import radical.utils   as ru

from .pty2pipe import PTY2Pipe


# ------------------------------------------------------------------------------
#
class PipedShell(object):

    # --------------------------------------------------------------------------
    #
    def __init__(self, uid, url, connect=True):
        '''
        We need the hosted shell/ssh/gsissh process to communicate over a proper
        pty, but at the same time, we want to channel communication via named
        pipes so that it can survive consumer failure.  We thus wrap the process
        into a `ptyprocess.PTYProcess` class, and add another process wrapper to
        proxy the pty I/O to the named pipes.  This PipedShell class hosts that
        proxy process: it will start the child process, and continuously pull
        and forward the I/O streams.  It should run in a *daemonized* process,
        as to survive consumer failuress (the consumer can reconnect to the
        pipe).

        Note that PTY's do not distinguish stdout and stderr - they only have
        input streams and output streams. We thus only create and maintain an
        input pipe and an output pipe.

        The consumer access to the named pipes is process and thread locked - we
        make no other attempt to coordinate concurrent communication with
        multiple consumers.
        '''

        self._url  = url
        self._uid  = uid
        self._base = ru.get_base(ns='rc', module='conn/%s' % self._uid)
        self._log  = ru.Logger('rc.conn.pipe')

        # I/O channels for the command interpreter (named pipes)
        self._fin  = '%s/pipe.in'  % self._base
        self._fout = '%s/pipe.out' % self._base
        self._fpid = '%s/pipe.pid' % self._base  # to store process pid
        self._furl = '%s/pipe.url' % self._base  # to store process pid
        self._flck = '%s/pipe.lck' % self._base

        # we buffer reads, specifically when we wait for complete lines
        self._lbuf = list()  # list of complete lines read from pipe.in
        self._dbuf = ''      # trailing data (no newline)  from pipe.in

        # initialize state variables: process pid and pipe handles
        self._pid  = None
        self._pin  = None
        self._pout = None

        # communication with the shell is, in general, synchronous - use a lock
        # file to coordinate channel use between processes, and an mt.Lock to
        # coordinate between threads.
        self._lockf = ru.Lockfile(self._flck)

        # NOTE: locking on construction is fine, but unlocking with `__del__`
        #       has two problems:
        #         - __del__ is not reliably called in Python
        #         - __del__ *is* called during daemonization
        #       so we end up calling `__del__` twice, one of which comes way too
        #       early.
        #       To shield from that, we keep the PID of the process around, in
        #       which this class was created, and `__del__` will only unlock
        #       when called within the same process.
        # FIXME: This does not help for the unreliable __del__ - the lockfile
        #        should time out or get invalidated on dead processes (use
        #        `Lockfile.owner()`?
        self._lpid = os.getpid()

        if connect:
            self.connect()


    # --------------------------------------------------------------------------
    #
    def connect(self):

        # lock during initialization
        self._lock(timeout=0)

        if not self._locked():
            raise RuntimeError('ptyshell to %s is in use' % self._url)

        # if we did not get an URL, see if we already know it from startinng
        # the pshell earlier.  If we got an url, make sure it's compatoble with
        # the url of an actiive pshell

        if self._url:
            active_url = self._read_url()

            if active_url and active_url != self._url:
                raise ValueError('proxy %s URL mismatch: [%s] [%s]'
                                % (self._uid, active_url, self._url))
        else:
            # no url - try to find fallback
            self._url = self._read_url()

            # we need some URL, either as arg or from a running proxy
            if not self._url:
                raise ValueError('no URL set, no active proxy url found')

        # try to reconnect to an existing process
        if not self._recover_state():

            # did not work - attempt to initialize a new process
            self._initialize_state()


    # --------------------------------------------------------------------------
    #
    def _initialize_state(self):

        self._log.debug('initialize')

        event = mp.Event()
        proc  = PTY2Pipe(self._uid, self._url, event)
        proc.start()

        # wait for the process to signal setup completion
        self._log.debug('wait for process')

        start = time.time()
        while not event.is_set():
            time.sleep(0.1)
            # FIXME: this is a very arbitrary timeout
            if time.time() > start + 10.0:
                raise RuntimeError('PTY2Pipe (%s) failed to start' % self._url)

        # store pid for reconnects and process health checks
        self._pid = proc.pid
        self._log.debug('pid: %s', self._pid)

        # connect the pipes created by PTY2Pipe
        # open on pin would block until the other end opens for reading - that
        # should have happened during setup already.  OTOH, the other side will
        # wait for use to read-open the pout channel.
        self._pin  = os.open(self._fin,  os.O_WRONLY | os.O_NONBLOCK, 0o600)
        self._pout = os.open(self._fout, os.O_RDONLY | os.O_NONBLOCK, 0o600)

        self._log.debug('open pin  w [%s]: %d', self._fin,  self._pin)
        self._log.debug('open pout r [%s]: %d', self._fout, self._pout)

        # this worked - store the state for later reconnects
        self._store_state()

        self._log.debug('initialize ok')


    # --------------------------------------------------------------------------
    #
    def __del__(self):

        self._log.debug('del %s', ru.get_stacktrace())

        if os.getpid() != self._lpid:
            # different process, likely after fork - don't unlock just yet
            return

        self.disconnect()

        self._log.debug('del ok')


    # --------------------------------------------------------------------------
    #
    def disconnect(self, _unlock=True):

        self._log.debug('disconnect')

        if self._pin is not None:
            try   : os.close(self._pin)
            except: self._log.exception('cannot close pin upon disconnect')

        if self._pout is not None:
            try   : os.close(self._pout)
            except: self._log.exception('cannot close pout upon disconnect')

        self._pin  = None
        self._pout = None

        if _unlock:
            try   : self._unlock()
            except: self._log.exception('cannot unlock upon disconnect')

        self._log.debug('disconnect ok')


    # --------------------------------------------------------------------------
    #
    def close(self):

        self._log.debug('close')

        # unlock follows below, after kill
        self.disconnect(_unlock=False)

        if not self._pid:
            try   : self._pid  = int(open(self._fpid, 'r').read().strip())
            except: self._log.exception('cannot get pid')

        if not self._pid:
            raise RuntimeError ('cannot extract pid for proxy %s')

        try   : os.kill(self._pid, signal.SIGKILL)
        except: self._log.exception('cannot kill p2p')

        self._clean_state()
        self._unlock()

        self._log.debug('close ok')


    # --------------------------------------------------------------------------
    #
    @property
    def pid(self):
        return self._pid

    @property
    def url(self):
        return self._url

    @property
    def connected(self):
        return bool(self._pin  is not None and
                    self._pout is not None)


    # --------------------------------------------------------------------------
    #
    def _read_url(self):
        '''
        read url from state store
        '''

        if os.path.isfile(self._furl):
            ret = open(self._furl, 'r').read().strip()
            return ret


    # --------------------------------------------------------------------------
    #
    def alive(self):

        try:
            assert(self._pid), 'no valid pid'

            # a poor-man's version of a process health check: send signal `0`.
            # This raises if the process does not exist
            assert(os.kill(self._pid, 0) is None), 'process is dead'

            # make sure we have valid I/O handles
            assert(self._pin),  'input  pipe missing'
            assert(self._pout), 'output pipe missing'

            # make sure the respective pipes exist
            assert(os.path.exists(self._fin)),  'named input  pipe is missing'
            assert(os.path.exists(self._fout)), 'named output pipe is missing'

        except Exception as e:
            self._log.debug('alive: False (%s)', e)
            return False

        return True


    # --------------------------------------------------------------------------
    # FIXME: try/except to trigger reconnect?
    # FIXME: move to rcu
    def write(self, data):

        while data:

            try:
                ret = os.write(self._pin, data)
                if ret:
                    data = data[ret:]

            except OSError as e:
                if e.errno != errno.EAGAIN:
                    raise


    # --------------------------------------------------------------------------
    # FIXME: try/except to trigger reconnect?
    # FIXME: add size parameter?
    # FIXME: move to rcu
    def read(self, timeout=None):
        '''
        unbuffered, non-blocking I/O
        '''

        data = self._dbuf
        self._dbuf = ''

        # check if there is something to read
        if select.select([self._pout], [], [], timeout)[0]:

            # gobble up data
            while True:
                data += os.read(self._pout, 1024)
                self._log.debug('data : %s', data)

                # check if there is more (non-blocking)
                if not select.select([self._pout], [], [], 0)[0]:
                    break

        data.replace('\r\n','\n')
        return data


    # --------------------------------------------------------------------------
    # FIXME: try/except to trigger reconnect?
    # FIXME: move to rcu
    def readline(self, timeout=None):
        '''
        buffered, non-blocking line-based I/O
        '''

        # check if we can return a line from the buffer
        if self._lbuf:
            return self._lbuf.pop(0)

        start = time.time()
        while True:

            # check if there is something to read
            chunk = self.read(timeout=timeout)

            if not chunk:
                # no new data within timeout - done
                return

            self._log.debug('chunk: %s', chunk)

            # got some data before timeout - try to extract complete lines from
            # data (accept universal newlines)
            dbuf = self._dbuf + chunk
            while True:
                if '\r\n' in dbuf: line, dbuf = dbuf.split('\r\n', 1)
                elif '\n' in dbuf: line, dbuf = dbuf.split('\n',   1)
                elif '\r' in dbuf: line, dbuf = dbuf.split('\r',   1)
                else: line = None

                if line: self._lbuf.append(line)
                else   : break

            self._dbuf = dbuf
            self._log.debug('dbuf : %s', self._dbuf)

            # check if we can return a line from the buffer
            if self._lbuf:
                return self._lbuf.pop(0)

            # got data, but no full line, yet - check if we have time to try
            # again
            if time.time() - start > timeout:
                # nope, out of time
                return


    # --------------------------------------------------------------------------
    #
    def _lock(self, timeout=None):

        self._log.debug('lock')
        ret = self._lockf.acquire(timeout=timeout, owner=ru.get_caller_name())
        self._log.debug('lock: %s', ret)

        if not ret:
            raise RuntimeError('Could not acquire lock: %s'
                               % self._lockf.get_owner())

        return ret


    # --------------------------------------------------------------------------
    #
    def _locked(self):

        if not self._lockf:
            self._log.debug('locked: -')
            return False

        ret = self._lockf.locked()
        self._log.debug('locked: %s', ret)
        return ret


    # --------------------------------------------------------------------------
    #
    def _unlock(self):

        if self._locked():
            self._log.debug('unlock: True')
            self._lockf.release()
        else:
            self._log.debug('unlock: False')


    # --------------------------------------------------------------------------
    #
    def _store_state(self):

        self._log.debug('store state')

        # The file format is very simple: two lines, first containing the URL,
        # pid of an existing ssh tunnel process.  Later iterations may also
        # add information about additional tunnels created on the original
        # channel, in order to re-establish those on reconnect.

        # make sure we are allowed to store state
        assert(self._locked()), 'need lock to store state'
        assert(self.alive()),   'need valid state to store it'

        # all is well - store state
        with open(self._fpid, 'w') as fout:
            fout.write('%d\n' % self.pid)

        # all is well - store state
        with open(self._furl, 'w') as fout:
            fout.write('%s\n' % self._url)

        self._log.debug('store state ok')


    # --------------------------------------------------------------------------
    #
    def _recover_state(self):
        '''
        Recover information about a running pty2pipe (and thus ptyshell) from
        the lockfile.  If that succeeds, check the health of that process.  If
        it lives, check if the named pipes exist and can be accessed.  If so,
        open the pipes.  If that works, return `True`.

        If any of the above steps fail, abort and return `False`.  In this case,
        the state is not recoverable - state should be cleaned, and the
        pty2pipe and ptyshell should be restarted.
        '''

        self._log.debug('recover state')

        try:
            assert(self._locked()),             'need lock to recover state'
            assert(os.path.isfile(self._fpid)), 'no state to recover'

            with open(self._fpid, 'r') as fin:
                data = fin.read()

            self._pid  = int(data.strip())
            self._pin  = os.open(self._fin,  os.O_WRONLY | os.O_NONBLOCK, 0o600)
            self._pout = os.open(self._fout, os.O_RDONLY | os.O_NONBLOCK, 0o600)

            assert(self.alive()), 'state recovery unsuccessful'

        except Exception:
            # could recover nothing, clean nonrecoverable state
            self._log.exception('state recovery failed')
            self._clean_state()
            return False

        # we did recover state - but the consumer will not see a prompt, as that
        # has been parsed away by the last consumer.  So we trigger a new prompt
        # by sending a newline (`enter`).
        self.write('\n')

        self._log.debug('recover state ok')
        return True


    # --------------------------------------------------------------------------
    #
    def _clean_state(self):
        '''
        Before we (re)start a new pty2pipe/ptyshell process, we clean out old
        pipes and any other state information.
        '''

        self._log.debug('clean state')

        if os.path.exists(self._fin):
            try   : os.unlink(self._fin)
            except: self._log.exception('cannot unlink fin')

        if os.path.exists(self._fout):
            try   : os.unlink(self._fout)
            except: self._log.exception('cannot unlink fout')

        if os.path.isfile(self._fpid):
            try   : os.unlink(self._fpid)
            except: self._log.exception('cannot unlink fpid')

        if os.path.isfile(self._furl):
            try   : os.unlink(self._furl)
            except: self._log.exception('cannot unlink furl')

        self._lockf.remove()

        self._log.debug('clean state ok')
        return True


# ------------------------------------------------------------------------------

