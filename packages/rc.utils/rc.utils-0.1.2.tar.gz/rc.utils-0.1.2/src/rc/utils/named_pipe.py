
__author__    = 'Andre Merzky <andre@merzky.net>'
__license__   = 'GNU AGPL.v3 *or* Commercial License'
__copyright__ = 'Copyright (C) 2019, RADICAL-Consulting UG'


import os
import time
import select

from .stream import Stream, SERVER, CLIENT


# ------------------------------------------------------------------------------
#
class NamedPipe(Stream):
    '''
    This class is a simple wrapper around a pair of unix named pipe.  It can
    create that pair of named pipe or open existing ones, and provides `read()`,
    `write()` on them.  `readline()` is provided for some convenience, all
    read/write access is thread save.

    A file descriptor on a unix named pipe can only be opened for reading *or*
    writing, and opening for `read` will block until the other end of the pipe
    is opened for `write`.  We thus create a *pair* of pipes for the two roles
    'server' and 'client', with the following convention:

      - a 'server' will create two named pipes 'pipe.1', 'pipe.2'
      - a 'server' will first open for 'pipe.1' read, then 'pipe.2' for write
      - a 'client' will wait until it sees the pipes created
      - a 'client' pipe will first open 'pipe.1' for write (thus unblocking the
        server), then 'pipe.2' for read (thus completing the two-way setup.

    With that convention, a 'server' will block until a client connects, and
    vice versa, and the connection is established once both `open()` calls
    return.
    '''

    # --------------------------------------------------------------------------
    #
    def __init__(self, name, role):
        '''
        Open an pipe in `Socket.sbox` under the given name.
        '''

        self._name = name

        Stream.__init__(self, role=role)

        # if name is an absolute path, use the dir part as sandbox - otherwise
        # use the `Stream._sbox` location as default
        if name[0] == '/': self._path = name
        else             : self._path = self._sbox + '/' + self._name

        # derive path names for both unidirectional pipes
        self._path_1 = self._path + '.1'
        self._path_2 = self._path + '.2'


    # --------------------------------------------------------------------------
    #
    def _open(self):

        with self._lock:

            if self._role == SERVER:

                if not os.path.exists(self._path):
                    # the mkfifo / chmod sequence has a race condition - but
                    # should be acceptable as
                    #   - the fifos live in the secured `Stream._sbox`
                    #   - only one reader / write are allowed on the fifo, and
                    #     connection bootstrap will fail if a third party
                    #     listens in
                    os.mkfifo(self._path_1, 0o600)
                    os.mkfifo(self._path_2, 0o600)

                    os.chmod(self._path_1, self._RWX)
                    os.chmod(self._path_2, self._RWX)

                self._fd_read  = open(self._path_1, 'r')
                self._fd_write = open(self._path_2, 'w')

            elif self._role == CLIENT:

                while True:
                    if os.path.exists(self._path_1) and \
                       os.path.exists(self._path_2) :
                        break

                    time.sleep(0.1)

                self._fd_write = open(self._path_1, 'w')
                self._fd_read  = open(self._path_2, 'r')

      # print('role: %s  read: %s  write: %s' % (self._role, self._fd_read.name,
      #     self._fd_write.name))


    # --------------------------------------------------------------------------
    #
    def _close(self):

        with self._lock:
            self._fd_read.close()
            self._fd_write.close()
            self._fd_read  = None
            self._fd_write = None


    # --------------------------------------------------------------------------
    #
    def _get(self, n):

        return self._fd_read.read(n)


    # --------------------------------------------------------------------------
    #
    def _put(self, data):

        self._fd_write.write(data)
        self._fd_write.flush()


    # --------------------------------------------------------------------------
    #
    def _test(self, timeout=None):

        with self._lock:
            r, _, _ = select.select([self._fd_read], [], [], timeout)
            print('select: %s: -%s-' % (r, 1))  # self._get(1)))
            if r: return True
            else: return False


# ------------------------------------------------------------------------------

