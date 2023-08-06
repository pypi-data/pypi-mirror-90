
__author__    = 'Andre Merzky <andre@merzky.net>'
__license__   = 'GNU AGPL.v3 *or* Commercial License'
__copyright__ = 'Copyright (C) 2019, RADICAL-Consulting UG'


import os
import time

from .stream import Stream, SERVER, CLIENT


# ------------------------------------------------------------------------------
#
class TCPSocket(Stream):
    # FIXME: this is just a copy of NamedPipe right now
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
    def __init__(self, path, role):
        '''
        Open an pipe at the given path.
        '''

        self._path   = path
        self._path_1 = path + '.1'
        self._path_2 = path + '.2'

        Stream.__init__(self, role=role)


    # --------------------------------------------------------------------------
    #
    def _open(self):

        with self._lock:

            if self._role == SERVER:

                if not os.path.exists(self._path):
                    os.mkfifo(self._path_1)
                    os.mkfifo(self._path_2)

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


# ------------------------------------------------------------------------------

