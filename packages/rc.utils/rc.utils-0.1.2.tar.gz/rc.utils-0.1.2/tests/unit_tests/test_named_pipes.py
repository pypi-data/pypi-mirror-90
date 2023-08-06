#!/usr/bin/env python3

import os
import time
import pytest
import tempfile
import unittest

import threading     as mt
import radical.utils as ru
import rc.utils      as rcu


# ------------------------------------------------------------------------------
#
class TestNamedPipe(unittest.TestCase):

    def test_named_pipe(self):

        # ----------------------------------------------------------------------
        def server(fname):
            server = rcu.NamedPipe(fname, role=rcu.SERVER)
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

            fname  = '%s/pipe' % dname

            thread = mt.Thread(target=server, args=[fname])
            thread.daemon = True
            thread.start()

            client = rcu.NamedPipe(fname, role=rcu.CLIENT)
            with client():

                client.write('start\n')

                line = client.readline()
                self.assertEqual(line, 'foo\n')

              # FIXME: why is this unreliable?
              # self.assertEqual(True, client.test(timeout=1.0))
                data = client.read(7)
                self.assertEqual(data, 'bar\nbuz')

                client.write('stop\n')

                with pytest.raises(RuntimeError):
                    data = client.read(1)

            self.assertEqual(client.state, rcu.CLOSED)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    tc = TestNamedPipe()
    tc.test_named_pipe()


# ------------------------------------------------------------------------------

