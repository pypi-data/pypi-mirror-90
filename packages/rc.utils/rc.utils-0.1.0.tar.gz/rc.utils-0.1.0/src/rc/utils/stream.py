
__author__    = 'Andre Merzky <andre@merzky.net>'
__license__   = 'GNU AGPL.v3 *or* Commercial License'
__copyright__ = 'Copyright (C) 2019, RADICAL-Consulting UG'


import os
import stat
import socket

import threading       as mt
import multiprocessing as mp

import radical.utils   as ru


# ------------------------------------------------------------------------------
#
NEW       = 'new'
BOUND     = 'bound'
LISTENING = 'listening'
CONNECTED = 'connected'
CLOSED    = 'closed'

SERVER    = 'server'
CLIENT    = 'client'


# ------------------------------------------------------------------------------
#
class Stream(object):
    '''
    The `Stream` class is a very simple abstracation around stream like data
    sources and sinks, such as named pipes, unix domain sockets or network
    connections (tcp sockets).  The main purpose is to provide a uniform state
    model and uniform methods for data I/O (read, write, readline, test, and
    select).
    '''

    # helper for `os.chmod()`
    _RWX = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR


    # --------------------------------------------------------------------------
    #
    def __init__(self, role):

        self._role       = role
        self._state      = NEW
        self._lock       = mt.RLock()  # use mp lock?

        assert(self._role in [SERVER, CLIENT]), role

        # create a private sandbox dir in `$RC_BASE` to store state, or to be
        # used as secure location for socket and pipe endpoints.
        self._base = ru.get_base('rc')
        self._sbox = self._base + '/utils/streams'

        ru.rec_makedir(self._sbox)
        os.chmod(self._sbox, self._RWX)


    # --------------------------------------------------------------------------
    #
    @property
    def state(self):
        return self._state

    @property
    def sbox(self):
        return self._sbox


    # --------------------------------------------------------------------------
    #
    def __call__(self, *args, **kwargs):
        '''
        call helper method for the context manager interface, which thus allows
        constructs like:

            with stream(foo, bar='buz'):
                do something

        where the arguments (`foo` and `bar`) are passed to an overloaded
        `_call()` method (which must have a matcghing signature).  The default
        implementation of that method does nothing.
        '''

        self._call(*args, **kwargs)
        return self


    # --------------------------------------------------------------------------
    #
    def _call(self, *args, **kwargs):
        '''
        method can be oveloaded with arbitrary signatures
        '''
        pass


    # --------------------------------------------------------------------------
    #
    def __enter__(self):
        '''
        Open the given Stream and close it when leaving the scope
        '''

        self.open()
        return self


    # --------------------------------------------------------------------------
    #
    def __exit__(self, x, y, z):
        '''
        When leaving the scope, close the context manager.  The documentation to
        `close()` applies.
        '''

        self.close()


    # --------------------------------------------------------------------------
    #
    def open(self):

        self._open()
        self._state = CONNECTED


    # --------------------------------------------------------------------------
    #
    def _open(self):

        # this method MUST be overloaded by the deriving class, as
        # implementation will differ depending on stream type and
        # client/server role
        raise NotImplementedError('deriving class must implement _open()')


    # --------------------------------------------------------------------------
    #
    def close(self):
        '''
        Close the held stream.  Any further read and write operations will
        raise an assertion error.
        '''
        self._close()
        self._state = CLOSED


    # --------------------------------------------------------------------------
    #
    def _close(self):

        # this method MUST be overloaded by the deriving class, as
        # implementation will differ depending on stream type and
        # client/server role
        raise NotImplementedError('deriving class must implement _close()')


    # --------------------------------------------------------------------------
    #
    def read(self, n):
        '''
        read `n` bytes from the stream.  The call will block until `n` bytes
        have been received.  The stream must be in `CONNECTED` state.  The call
        is thread-safe (locked by a multithreading lock).
        '''

        with self._lock:

            assert(self._state == CONNECTED), self._state

            data = ''
            while len(data) < n:
                chunk = self._get(n - len(data))
                if not chunk:
                    raise RuntimeError('read failed - disconnected?')
                data += chunk

            return data


    # --------------------------------------------------------------------------
    #
    def readline(self):
        '''
        read all bytes from the stream until a linebreakis found.  The call will
        block, the linebreak is returned in the resulting list of bytes.  The
        stream must be in `CONNECTED` state.  The call is thread-safe (locked by
        a multithreading lock).
        '''

        with self._lock:

            assert(self._state == CONNECTED), self._state

            line = ''
            while True:
                char = self._get(1)
                if not char:
                    raise RuntimeError('connection closed')
                line += char
                if char == '\n':
                    return line


    # --------------------------------------------------------------------------
    #
    def write(self, data):
        '''
        write given bytes to the stream.  The call will block until write is
        complete.  The stream must be in `CONNECTED` state.  The call is
        thread-safe (locked by a multithreading lock).
        '''

        with self._lock:

            assert(self._state == CONNECTED), self._state

            self._put(data)

    # --------------------------------------------------------------------------
    #
    def test(self, timeout=None):

        with self._lock:
            return self._test(timeout=timeout)


# ------------------------------------------------------------------------------

