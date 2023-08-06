#!/usr/bin/env python3

import os
import time
import pytest
import tempfile
import unittest

import threading     as mt
import radical.utils as ru

import rc.io


# ------------------------------------------------------------------------------
#
class TestUDS(unittest.TestCase):

    def test_uds(self):

        # ----------------------------------------------------------------------
        def server(fname):
            server = rc.io.UnixDomainSocket(fname, role=rc.io.SERVER)
            server.open()
            try:
                line = server.readline()
                self.assertEqual(line, 'start\n')

                server.write('foo\nbar')
                server.write('\nbuz')

                line = server.readline()
                self.assertEqual(line, 'stop\n')
            except Exception:
                ru.print_exception_trace()
                raise
            finally:
                server.close()
        # ----------------------------------------------------------------------

        with tempfile.TemporaryDirectory(prefix='tmp.rc.') as dname:

            fname  = '%s/uds' % dname

            thread = mt.Thread(target=server, args=[fname])
            thread.daemon = True
            thread.start()

            client = rc.io.UnixDomainSocket(fname, role=rc.io.CLIENT)
            with client():

                client.write('start\n')

                line = client.readline()
                self.assertEqual(line, 'foo\n')

                self.assertEqual(True, client.test(timeout=2.0))
                data = client.read(7)
                self.assertEqual(data, 'bar\nbuz')

                client.write('stop\n')

              # with pytest.raises(RuntimeError):
              #     data = client.read(1)

            self.assertEqual(client.state, rc.io.CLOSED)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    tc = TestUDS()
    tc.test_uds()


# ------------------------------------------------------------------------------

