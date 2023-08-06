
__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


import os
import sys
import select
import shutil
import termios

import radical.utils   as ru

from .tunnel      import Tunnel
from .piped_shell import PipedShell
from .constants   import _PROMPT
from .constants   import _SOCKS5_EP


# ------------------------------------------------------------------------------
#
class Proxy(object):
    '''
    We frequently face the problem that a network connection cannot be directly
    established due to firewall policies.  At the same time, establishing ssh
    tunnels manually can be cumbersome, as that needs activity by every user,
    coordination of used port numbers, out-of-band communication of tunnel
    settings, etc.

    This class eleviates that problem for the scope of the RC stack.  It
    expects two user level settings:

        export RC_PROXY_URL=ssh://host/

    to specify a suitable tunnel host.  When being used by some layer in the
    RC stack, this class will:

        - search a free local port;
        - establish a SOCKS5 tunnel to the given host, binding it to the given
          port;
        - additionally establish, on demand, required (non-SOCKS) application
          tunnels over that SOCKS tunnel.

    The existence of the SOCKS tunnel is recorded in the file

        `$HOME/.rc/utils/proxy.<host>[.<name>]`

    which contains information about the used local port.  That file will
    disappear when the proxy disappears.  The `[.<name>]` part is used for
    direct application tunnels established over the original socks proxy tunnel.
    `name` is expected to be a unique identifyer.  The proxy is expected to live
    until it is explicitly closed.

    If no proxy is given, the methods in this class are NOOPs - it can thus
    transparently be used for proxied and direct connections.


    Requirements:
    -------------

      * passwordless ssh login needs to be configured from localhost to the
        proxy host (but see TODOs below)
      * the proxy host must have these settings in `/etc/ssh/sshd_config`:

            GatewayPorts       yes
            AllowTcpForwarding yes

    TODO:
    -----

      * gsissh support
      * support different auth mechanisms (user/key, public key, encrypted key,
        ssh agent, myproxy, KeyFobs, TFA, etc - see SAGA security contexts)


    Usage:
    ------

        # connect to `http://www.google.com/` (port 80), SOCKS enabled client
        proxy   = ru.Proxy(timeout=300)
        tgt_url = proxy.url(socks=True, 'http://www.google.com/')
        print(tgt_url)
          --> http://localhost:10000/
        client.connect(tgt_url)

        # connect to `mongodb://www.mlab.com:12017/rp`, client is *not* able to
        # use SOCKS
        proxy = ru.Proxy()
        print proxy.url(socks=False, `mongodb://www.mlab.com:12017/rp`)
          --> mongodb://localhost:10001/rp

        proxy.close() / gc


    We  will also provide a command line tool which supports similar operations
    in the shell:

        # connect to `http://www.google.com/` (port 80), SOCKS enabled client
        wget `rc-proxy --socks=True 'http://www.google.com/'`

        # connect to `mongodb://foobar.mlab.com:12017/rp`. client is *not* able
        # to use SOCKS
        mongo `rc-proxy --socks=False 'foobar.mlab.com:12017' rp`
    '''


    # we use netcat and its derivates to establish the proxy connection.  The
    # dict below abstracts the syntax differences for the different flavors.
    #
    #     nc     -X 5 -x 127.0.0.1:10000 %h %p
    #     netcat -X 5 -x 127.0.0.1:10000 %h %p
    #     ncat   --proxy-type socks5 --proxy 127.0.0.1:10000 %h %p
    #     socat  - socks:127.0.0.1:%h:%p,socksport=10000
    #
    _tunnel_proxies = {
        'ncat'   : 'ncat    --proxy-type socks5 '
                           '--proxy 127.0.0.1:%(proxy_port)d %%%%h %%%%p',
        'nc'     : 'nc      -X 5 -x 127.0.0.1:%(proxy_port)d %%%%h %%%%p',
        'netcat' : 'netcat  -X 5 -x 127.0.0.1:%(proxy_port)d %%%%h %%%%p',
        'socat'  : 'socat   - socks:127.0.0.1:%%%%h:%%%%p,'
                             'socksport=%(proxy_port)d'
    }


    # --------------------------------------------------------------------------
    #
    def __init__(self, pid, url=None, connect=True):
        '''
        Create a new Proxy, ie., a new PTY endpoint to the target host.  This
        will use the given url to connect to the target machine, establish a PTY
        channel, bootstrap a small shell based command interpreter.  This class
        communicates with the pty channel over a pair of named pipes.  The
        spawned process and the pipes can survive this class, and any new
        instance can reconnect to them instead of recreating them.

        If this class finds that a proxy already exists for the given URL, the
        health of that proxy is checked, and if it is still function and not
        used by any other process, the class will reconnect to that existing
        proxy.  Existing proxies are stored in  `$HOME/.rc/conn/<pid>`
        (or more precisely, from `rc_base/conn/...`), where pid and pipes
        of the connecting processes are stored.

        The communication channels are thread and process locked - only one
        process can use them at any time.  Since the IDs of the channel only
        depend on scheme, host, port, scheme and user ID, any additional process
        which wishes to communicate with that endpoint needs the cooperation of
        the channel owner to establish an additional out-of-band communication
        channel (see `tunnel()` method).

        supported schemas: ssh, gsissh, sh
        '''

        # information about established proxy endpoints are stored on disk, so
        # that proxies can be picked up and reconnected to in case of failures
        #
        # TODO: lock proxies so that only one client instance can use them at
        #        any time, or make sure that multi-tenant use works
        self._log  = ru.Logger(name='rc.conn.proxy')
        self._uid  = pid
        self._base = ru.get_base(ns='rc', module='conn/%s' % self._uid)

        # keep track of tunnels created on this proxy instance
        self._tunnels = list()  # tunnels can origin from any intermediate hop


        self._log.debug('request piped shell for %s : url %s', self._uid, url)

        # start PTYShell in a Pipe translator.  This will reconnect to any
        # running shell for that url target, or create a new one.
        self._pshell = PipedShell(url=url, uid=self._uid, connect=connect)

        if connect:

            # bootstrap the communication by finding the prompt.  Interaction with
            # the end user may be needed if the shell needs to establish a new
            # connection, so `initialize()` will forward all non-prompt output from
            # the shell to stdout, and will in return forward all input from stdin
            # to the shell.
            ret = self._find_prompt(stdin_fd=sys.stdin, stdout_fd=sys.stdout,
                                    echo=False)

            # turn off echo in the remote shell
            self.cmd('stty -echo')
            self._log.debug('find prompt returned: [%s]', ret)


    # --------------------------------------------------------------------------
    #
    @property
    def uid(self):

        return self._uid


    # --------------------------------------------------------------------------
    #
    @property
    def url(self):

        return self._pshell.url


    # --------------------------------------------------------------------------
    #
    def close(self):

        self._pshell.close()

        shutil.rmtree(self._base)


    # --------------------------------------------------------------------------
    #
    def cmd(self, command):

        if not self._pshell.connected:
            raise RuntimeError('cannot run cmd on disconnected proxy')

        ret = self._find_prompt(stdin='%s\n' % command.rstrip('\n'))
        return ret


    # --------------------------------------------------------------------------
    #
    def get_tunnel(self, url):

        if not self._pshell.connected:
            raise RuntimeError('cannot tunnel on disconnected proxy')

        ep = self._pshell.get_tunnel_ep(url)
        t  = Tunnel(ep)
        self._tunnels.append(t)


    # --------------------------------------------------------------------------
    #
    def _getecho(self, fd):

        try:
            attr = termios.tcgetattr(fd)

            return bool(attr[3] | ~termios.ECHO)

        except:
            return None


    # --------------------------------------------------------------------------
    #
    def _setecho(self, fd, state):

        try:
            attr = termios.tcgetattr(fd)

            if state: attr[3] = attr[3] |  termios.ECHO
            else    : attr[3] = attr[3] & ~termios.ECHO

            termios.tcsetattr(fd, termios.TCSANOW, attr)
        except:
            pass


    # --------------------------------------------------------------------------
    #
    def _find_prompt(self, stdin='', stdin_fd=None, stdout_fd=None, echo=True):
        '''
        Continuously read from the pshell until a prompt is found.  Return all
        data found until then (excluding the prompt itself).

        If `stdin` is defined, send that data to the pshell before starting to
        read.

        If `stdin_fd` is defined, continuously check for data on that fd, and send
        any data found to the pshell.

        If `stdout_fd` is defined, send all data found to that fd.  This does
        not affect the data returned by this call.
        '''

        # FIXME: add timeout

        self._log.debug('find prompt 1: %s %s', stdin_fd, stdout_fd)

        # convert file streams to file descriptors
        if hasattr(stdin_fd,  'fileno'): stdin_fd  = stdin_fd.fileno()
        if hasattr(stdout_fd, 'fileno'): stdout_fd = stdout_fd.fileno()

        self._log.debug('find prompt 2: %s %s', stdin_fd, stdout_fd)

        old_echo = self._getecho(stdin_fd)
        if not echo:
            if stdin_fd is not None:
                self._setecho(stdin_fd, False)

        try:
            # push inut to pshell
            if stdin:
                self._log.debug('send [%s]', stdin)
                self._pshell.write(stdin)

            data = ''
            while True:

                if not self._pshell.alive():
                    self._log.warn('pshell died')
                    break  # process terminated

                # check if we can read anything
                chunk = self._pshell.read(timeout=0.1)

                if chunk:
                    self._log.debug('read : [%s]', chunk)
                    data += chunk

                    # did we get the prompt?
                    if data.endswith(_PROMPT):
                        self._log.info('found prompt')

                        # remove the prompt from the data
                        data = data[:-len(_PROMPT)]

                        # do we need to send a remainder of `chunk` to `stdout_fd`?
                        if stdout_fd is not None:
                            chunk = chunk[:-len(_PROMPT)]
                            os.write(stdout_fd, chunk)
                          # os.fsync(stdout_fd)

                        return data

                    # write chunkd stdout
                    if stdout_fd is not None:
                        os.write(stdout_fd, chunk)
                      # os.fsync(stdout_fd)

                # check if the user wants us to send some stdin
                if stdin_fd is not None:
                    self._log.debug('Send %d?', stdin_fd)
                    d_in = self._read(fd=stdin_fd, timeout=0)
                    if d_in:
                        self._log.debug('Send [%s]', d_in)
                        self._log.debug('stdin: [%s]', d_in)
                        self._pshell.write(d_in)

        finally:
            if old_echo and not echo:
                self._setecho(stdin_fd, True)

        # the above loop breaks on process dead.  Should also break on timeout
        raise RuntimeError('could not open shell to %s' % self.url)


    # --------------------------------------------------------------------------
    #
    def _read(self, fd, timeout=None):
        '''
        unbuffered, non-blocking I/O
        '''

        # check if there is something to read
        if select.select([fd], [], [], timeout)[0] == [fd]:

            data = ''

            # gobble up data
            while True:
                data += os.read(fd, 1024)

                # check if there is more (non-blocking)
                if not select.select([fd], [], [], 0)[0]:
                    break

            data.replace('\r\n','\n')
            return data


# ------------------------------------------------------------------------------

