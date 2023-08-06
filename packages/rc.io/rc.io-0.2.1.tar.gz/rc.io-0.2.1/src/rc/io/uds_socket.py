
__author__    = 'Andre Merzky <andre@merzky.net>'
__license__   = 'GNU AGPL.v3 *or* Commercial License'
__copyright__ = 'Copyright (C) 2019, RADICAL-Consulting UG'


import os
import time
import socket
import select

from .stream import Stream, SERVER, CLIENT

import radical.utils as ru


# ------------------------------------------------------------------------------
#
class UnixDomainSocket(Stream):
    '''
    This class is a simple wrapper around a Unix Domain Socket (USD), and
    provides `write()`, `read()` and `readline()` via it's `Stream` base class.
    The class distingushes 'server' and 'client' roles, where the 'server' is
    always responsible for creating the USD.
    '''

    # --------------------------------------------------------------------------
    #
    def __init__(self, name, role):
        '''
        Open an UDS in `Socket.sbox` under the given name.
        '''

        self._name = name

        Stream.__init__(self, role=role)

        # if name is an absolute path, use the dir part as sandbox - otherwise
        # use the `Stream._sbox` location as default
        if name[0] == '/': self._path = self._name
        else             : self._path = self._sbox + '/' + self._name


    # --------------------------------------------------------------------------
    #
    def _open(self):

        with self._lock:

            if self._role == SERVER:

                if os.path.exists(self._path):
                    os.unlink(self._path)

                self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._sock.bind(self._path)
                self._sock.listen(1)
                self._conn, self._client_addr = self._sock.accept()

            elif self._role == CLIENT:

                # wait for a bit (5 seconds) for the endpoint to appear
                start = time.time()
                while not os.path.exists(self._path):
                    if time.time() - start > 5:
                        break
                    time.sleep(0.1)

                if not os.path.exists(self._path):
                    raise ValueError('no endpoint at %s' % self._path)

                self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._sock.connect(self._path)
                self._conn = self._sock


    # --------------------------------------------------------------------------
    #
    def _close(self):

        with self._lock:
            self._conn.close()


    # --------------------------------------------------------------------------
    #
    def _get(self, n):

        # TODO: read into larger chunks and buffer superfluous data

        with self._lock:
            data = ''

            while True:
                data += ru.as_string(self._conn.recv(n - len(data)))
                if len(data) == n:
                    return data


    # --------------------------------------------------------------------------
    #
    def _put(self, data):

        with self._lock:
            self._conn.sendall(ru.as_bytes(data))


    # --------------------------------------------------------------------------
    #
    def _test(self, timeout=None):

        with self._lock:
            r, _, _ = select.select([self._conn], [], [], timeout)
            if r: return True
            else: return False


# ------------------------------------------------------------------------------

