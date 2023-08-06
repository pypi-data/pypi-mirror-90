
__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


import os
import time
import shlex
import socket
import psutil

import ptyprocess    as pp
import radical.utils as ru

from .tunnel import Tunnel

from .constants import _PORTS
from .constants import _PROMPT
from .constants import _SOCKS5_EP


# ------------------------------------------------------------------------------
#
class PTYShell(object):

    # --------------------------------------------------------------------------
    #
    def __init__(self, url, cwd):
        '''
        As mentioned in the docstring to `pty_2_pipe`, we wrap the target
        shell/ssh/gsissh process into a `ptyprocess.PTYProcess` class.  This
        method is doing just that, and returns a tuple of the object instance
        and its pty file descriptor used for communication (both for input and
        output).

        This method also monkey-patches the `ptyprocess.PTYProcess` class with
        methods for async I/O, async wait, and async state checks.  As such, it
        is dependent on internals of the `PTYProcess` implementation - but
        fortunately only depends on the availability of the pty file descriptor
        and the child's process ID.
        '''

        self._log  = ru.Logger('rc.conn.pty')
        self._log.debug('create pty shell for %s', url)

        self._url  = ru.Url(url)
        self._pwd  = cwd
        self._proc = None
        self._mode = self._url.scheme
        self._user = self._url.username
        self._host = self._url.host
        self._port = self._get_port(self._url)

        try:
            self._initialize()

        except:
            self._log.exception('could not initialize pty shell')
            raise


    # --------------------------------------------------------------------------
    #
    def _initialize(self):

        # we basically want to run:
        #
        #   SHELL='/usr/bin/env PS1="PROMPT> " /bin/sh +m -i'
        #
        #   +m : turn off job control ( we don't have a full pty)
        #   -i : force interactive shell
        #
        # For schema `sh`, this is exactly what we do.  For ssh, we need to
        # handle password exchange, dynamic port forwarding, and some ssh
        # config settings:
        #
        #   -D <port>  : dynamic app-level port forwarding over port <port>
        #   -D <socket>: dynamic app-level port forwarding over unix xocket
        #
        # For -D <port>, we actually use `127.0.0.1:<port>` so that the
        # forwarding port is only visible on localhost.  The port for `-D` must
        # be unused.  We try t o find such a port with `self._find_port`, but
        # a race exists between finding that port amd using it.
        #
        # NOTE: no attempt is made to secure access to that port from other
        #       users / applications on the local machine.
        #
        #       USE THIS SOFTWARE ONLY ON MACHINES YOU TRUST!
        #
        # Some versions of ssh seem to support specifying a unix domain socket
        # as target for `-D`, although that is undocumented (this is only
        # documented for port forwarding via `-L` and `-R`.  That mode has the
        # advantage that we can apply file system permissions to the socket,
        # making sure that only the current user can access it for forwarding
        # connections.  This is not possible with a port.  We thus prefer this
        # option where available.
        #
        # TODO: probe ssh on startup for this option (right now we hardcode it)
        # NOTE: -D sockets seem to ignore `StreamLocalBindUnlink`, so we need to
        #       ensure cleanup manually.
      # self._d_mode = 'port'
        self._d_mode = 'socket'

        self._log.debug('d_mode: %s', self._d_mode)


        # Other ssh config options:
        #
        #   -o "RequestTTY force"         : pty for interactive auth (-t -t)
        #   -o "EscapeChar none"          : fully channel transparent (-e none)
        #   -o "ExitOnForwardFailure yes" : fail loudly on port forwarding
        #   -o "ServerAliveCountMax 60"   : stay alive longer (60 tries)
        #   -o "ServerAliveInterval 60"   : stay alive longer (try every 60s)
        #   -o "TCPKeepAlive no"          : rely on ServerAlive messages
        #   -o "StreamLocalBindMask 0177" : sockets only accessible to user
        #   -o "StreamLocalBindUnlink yes": sockets unlinked when terminating

        opts  = ' -t -t'
     ## opts  = ' -o "RequestTTY force"'
     ## opts += ' -e none'
     ## opts += ' -o "EscapeChar none"'
     ## opts += ' -o "ExitOnForwardFailure yes"'
     ## opts += ' -o "ServerAliveCountMax 60"'
     ## opts += ' -o "ServerAliveInterval 60"'
     ## opts += ' -o "TCPKeepAlive no"'
        opts += ' -o "StreamLocalBindMask 0177"'
        opts += ' -o "StreamLocalBindUnlink yes"'

        # the basic command setup is the same for port and socket modes
        sh_cmd = '/usr/bin/env PS1="%s" /bin/sh +m -i' % _PROMPT

        if self._mode in ['sh']:

            ssh_cmd = ''


        elif self._mode in ['ssh', 'gsissh']:

            if   self._mode == 'ssh'   : ssh_cmd = 'ssh'
            elif self._mode == 'gsissh': ssh_cmd = 'gsissh'

            if self._user:
                ssh_cmd += ' -l %s' % self._user

            ssh_cmd += ' %s -p %d %s' % (opts, self._port, self._host)

        self._log.debug('ssh cmd: %s', ssh_cmd)
        self._log.debug('sh  cmd: %s', sh_cmd)


        if not ssh_cmd:

            cmd = sh_cmd


        elif ssh_cmd and self._d_mode == 'port':

            # we can find out what port is free to use for `-D`, but there is
            # always a race between finding that port and using it, so there is
            # no choice than to try until we succeed.
            #
            # FIXME: this is not fast
            #
            port_min = 49152   # use ephemeral ports
            port_max = 65535   # port numbers are unsigned int

            while port_min <= port_max:

                self._d_port = self._find_port(iface='127.0.0.1',
                                               port_min=port_min,
                                               port_max=port_max)
                ssh_cmd += ' %s -D 127.0.0.1:%d' % (opts, self._d_port)
                cmd      = "%s '%s'" % (ssh_cmd, sh_cmd)

                self._log.debug('run: %s', cmd)
                args = shlex.split(cmd)
                self._proc = pp.PtyProcess.spawn(args, cwd=self._pwd,
                                                       echo=False,
                                                       preexec_fn=None,
                                                       dimensions=(24, 80))

                # give ssh a bit to figure out if the port is usable
                # FIXME: this is an arbitrary timeout - should we wait until we
                #        see the first byte of output, maybe?
                time.sleep(0.1)
                if self.alive:
                    break

                self._log.warn('pty process failed (dport: %d)', self._d_port)
                port_min += 1
                continue


        elif ssh_cmd and self._d_mode == 'socket':

            # make sure the socket location does not exist in `pwd`, and go!
            self._d_sock = '%s/%s' % (self._pwd, _SOCKS5_EP)
            self._log.debug('d_sock: %s', self._d_sock)

            if os.path.exists(self._d_sock):
                try   : os.unlink(self._d_sock)
                except: pass

            if os.path.exists(self._d_sock):
                raise RuntimeError('socket path already exists')

            ssh_cmd += ' %s -D %s' % (opts, self._d_sock)
            cmd      = "%s '%s'" % (ssh_cmd, sh_cmd)

            self._log.debug('run: %s', cmd)
            args = shlex.split(cmd)
            self._proc = pp.PtyProcess.spawn(args, cwd=self._pwd,
                                                   echo=False,
                                                   preexec_fn=None,
                                                   dimensions=(24, 80))

            # give ssh a bit to figure out if the port is usable
            # FIXME: this is an arbitrary timeout - should we wait until we see
            #        the first byte of output, maybe?
            time.sleep(0.1)
            if not self.alive:
                raise RuntimeError('shell process failed')

        self._log.info('pty process spawned: %s : %s : %s',
                       self.pid, self.pty, self.alive())


    # --------------------------------------------------------------------------
    #
    def request_tunnel(self, name, url, multiplex=False):

        return Tunnel(self, name, url, multiplex)


    # --------------------------------------------------------------------------
    #
    @property
    def pty(self):

        return self._proc.fd


    # --------------------------------------------------------------------------
    #
    @property
    def pid(self):

        return self._proc.pid


    # --------------------------------------------------------------------------
    #
    @property
    def dsock(self):

        if self._d_mode == 'socket':
            return self._d_sock


    # --------------------------------------------------------------------------
    #
    @property
    def dport(self):

        if self._d_mode == 'port':
            return self._d_port


    # --------------------------------------------------------------------------
    def alive(self):

        return self._proc.isalive()


    # --------------------------------------------------------------------------
    #
    def _get_port(self, url):

        # FIXME: moove to ru.URL

        if url.schema in ['sh', '', None]:
            return None

        port = url.port
        if not port:
            port = _PORTS.get(url.schema)

        if not port:
            try:
                port = socket.getservbyname(url.schema)
            except socket.error:
                pass

        if not port:
            raise ValueError('cannot handle "%s" urls' % url.schema)

        return port


    # --------------------------------------------------------------------------
    #
    def _find_port(self, iface=None, port_min=None, port_max=None):
        '''
        Inspect the OS for tcp connection usage, and pick an unused port in the
        private, ephemeral port range between 49152 and 65535.  By default we
        check all interfaces, but an interface can also be specified as optional
        argument, identified by its IP number.

        NOTE: this mechanism does not *reserve* a port, so there is a race
        between finding a free port and using it.
        '''

        # FIXME: move to RU

        if not port_min: port_min = 49152
        if not port_max: port_max = 65535

        used_adr     = [c.laddr for c in psutil.net_connections(kind='tcp')]
        if iface:
            used_adr = [x       for x in used_adr if x[0] == iface]
        used_ports   = [x[1]    for x in used_adr]

        for port in range(port_min, port_max):
            if port not in used_ports:
                return port

        return None


# ------------------------------------------------------------------------------

