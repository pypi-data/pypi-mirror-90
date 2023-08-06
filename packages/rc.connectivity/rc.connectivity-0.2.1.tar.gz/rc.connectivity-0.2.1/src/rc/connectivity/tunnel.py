
__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


import weakref

import radical.utils as ru


# ------------------------------------------------------------------------------
#
class Tunnel(object):
    '''
    Tunnel holds information on a tunnel endpoint which was created
    via some proxy.
    '''

    # Once the pty shell is up, a tunnel endpoint can be requested.  For plain
    # sh, the endpoint will be a socat forward from the original host/port
    # endpoint to a UNIX domain socket.  For ssh/gsissh, we use `rc.rfc.1928` to
    # negotiate a SOCKS5 connection setup, and forward the resulting channel to
    # a named pipe.
    #
    # In both cases, a process will be spawned (`socat` or `rc.socksify`), and
    # the tunnel will stay alive as long as that process lives.  We will keep
    # track of the process and watch it.  If the process unexpectedly dies, it
    # will be restarted - any custumer of the resulting channel SHOULD thus be
    # able to recover from connection restart.  The tunnel is also recreated if
    # the original ssh channel dies and is restarted, and it is also recreated
    # on process restart / reconnect.
    #
    # `name` uniquely identifies the tunnel.  If a tunnel process for that name
    # exists and is healthy, the endpoint will be r

    def __init__(self, name, url, proxy):

        self._name   = name
        self._url    = ru.Url(url)
        self._proxy  = weakref.ref(proxy)  # avoid circular deps

        try:
            assert(int(self._url.port)),  'need valid port for tunnel ep'
            assert(self._url.is_local()), 'tunnel EP must be local'

        except Exception as e:
            ValueError('cannot use url [%s] as tunnel endpoint: %s' % (url, e))


    # --------------------------------------------------------------------------
    #
    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def port(self):
        return self._url.port

    @property
    def proxy(self):
        return self._proxy()

    @property
    def socks5(self):
        return self._socks5


# ------------------------------------------------------------------------------

