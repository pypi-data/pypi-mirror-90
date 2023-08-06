
__author__    = 'RADICAL-Consulting'
__email__     = 'devel@radical-consulting.com'
__copyright__ = 'Copyright date 2019-2021'
__license__   = 'LGPL.v3 *or* commercial license'


import os
import sys
import time
import errno
import select

import setproctitle    as spt

import radical.utils   as ru

from .pty_shell import PTYShell

_POLLDELAY = 0.1


# ------------------------------------------------------------------------------
#
class PTY2Pipe(ru.Daemon):

    # --------------------------------------------------------------------------
    #
    def __init__(self, uid, url, setup_ev):
        '''
        This method runs in a daemonized child process.  It hosts the PTYShell
        instance and will continuously pull/push I/O from/to the shell to a pair
        of named pipes.  This method will only finish when (a) it is being
        forcefully killed, or (b) the pty shell finishes / dies.
        '''

        self._uid = uid
        self._url = url
        self._ev  = setup_ev
        self._log  = ru.Logger('rc.conn.p2p')

        self._base = ru.get_base(ns='rc', module='conn/%s' % self._uid)
        self._outf = '%s/p2p.out' % self._base
        self._errf = '%s/p2p.err' % self._base

        ru.Daemon.__init__(self, stdout=self._outf, stderr=self._errf)


    # --------------------------------------------------------------------------
    #
    def _initialize(self):

        self._base  = ru.get_base(ns='rc', module='conn/%s' % self._uid)
        self._log   = ru.Logger('rc.conn.p2p')
        spt.setproctitle('rc.p2p.%s' % self._uid)

        # redirect I/O
        sys.stdout  = open('%s/p2p.out' % self._base, 'w')
        sys.stderr  = open('%s/p2p.err' % self._base, 'w')

        # create the pty shell, obtain its pty fd
        self._shell = PTYShell(self._url, cwd=self._base)
        self._pty   = self._shell.pty

        # create the named pipes
        self._fin   = '%s/pipe.in'  % self._base
        self._fout  = '%s/pipe.out' % self._base

        os.mkfifo(self._fin,  0o600)
        os.mkfifo(self._fout, 0o600)

        # open the reading end on the inpuy pipe non-blocking - after that,
        # a consumer WRONLY open should succeed.
        self._pin = os.open(self._fin, os.O_RDONLY | os.O_NONBLOCK, 0o600)
        self._log.debug('open pin  r [%s]: %d', self._fin, self._pin)

        # A `WRONLY` open on fout will block unless a consumer connects on
        # the reading end.  We will not try here, but delay the pout setup
        # and buffer any output from the pty until we actually want to
        # write, and then attempt to open it and send the buffer.
        self._pout = None
        self._buf  = ''

        # setup is done - notify parent process, and start pushing data
        self._log.debug('set ev')
        self._ev.set()
        self._log.debug('set ev done')


    # --------------------------------------------------------------------------
    #
    def run(self):


        # any unexpected exception in the loop will lead to termination
        try:
            self._initialize()

            while True:
                # forever pull input, output from the pty, and proxy those to
                # the input and output pipes

                # don't use read/write timeouts - instead, sleep a tiny bit if
                # *neither* channel yields any data.  This is less effective
                # than a proper timeout, but avoids preferring one direction
                # over the other (or stalling both).

                # fetch data from both channels
                d_in  = self._read(self._pin, timeout=0)
                d_out = self._read(self._pty, timeout=0)

                if d_in : self._log.debug('d_in : %s', d_in)
                if d_out: self._log.debug('d_out: %s', d_out)

                # forward input - make sure all is send
                d_in = self._fwd_pin(d_in)

                # forward output - and on the way recover from any consumer
                # side disconnect / reconnect.
                self._fwd_pout(data=d_out)

                # avoid busy poll
                if not d_in and not d_out:
                    time.sleep(_POLLDELAY)

                # check process state, and break the loop if it died
                if not self._shell.alive():
                    self._log.debug('shell died')
                    break

        except Exception:
            self._log.exception('error in main loop')

        except:
            self._log.error('leaving in main loop: %s',
                    ru.print_exception_trace())
            for line in ru.get_stacktrace():
                self._log.debug(line.strip())

        finally:

            # we get here when the pty process is dead - close the pipes to
            # inform consumers, and erase all traces of this process - any
            # new consumer needs to pull up a new process chain
            try   : os.close(self._pin)
            except: pass
            try   : os.close(self._pout)
            except: pass


    # --------------------------------------------------------------------------
    #
    def _read(self, fd, timeout=None):
        '''
        unbuffered, non-blocking I/O
        '''

        # check if there is something to read
        if select.select([fd], [], [], timeout)[0]:

            data = ''

            # gobble up data
            while True:

                chunk = os.read(fd, 1025)

                if not len(chunk):
                    break

                data += chunk

                # check if there is more (non-blocking)
                if not select.select([fd], [], [], 0)[0]:
                    break

            data.replace('\r\n','\n')
            return data


    # --------------------------------------------------------------------------
    #
    def _fwd_pout(self, data):
        '''
        Helper to open / reopen / write / buffer / flush the output pipe: If
        `self._pout` is not yet open, open it.  If it looks like a broken pipe
        (customer hangup),re-open it.  append any date to be written to the
        buffer, and try to write as much as possible.
        '''

        # append data to write buffer
        if data:
            self._buf += data

        # check if we have anything to do, really
        if not self._buf:
            return

        # do we need to (re)open for first write?
        if not self._pout:
            self._log.debug('open pout w [%s]', self._fout)
            try:
                self._pout = os.open(self._fout, os.O_WRONLY | os.O_NONBLOCK, 0o600)
                self._log.debug('open pout w [%s]: %d', self._fout, self._pout)

            except OSError as e:
                if e.errno != errno.ENXIO:
                    raise

                # can't (re)open right now - defer write attempts
                self._log.debug('open pout failed - delay output')
                return

        # perform as many writes as needed to empty the buffer
        while self._buf:

            self._log.debug('buf: %s', self._buf)
            try:
                self._log.debug('write output')
                ret = os.write(self._pout, self._buf)

                if not ret:
                    # could not write anything - handle like EAGAIN
                    self._log.warn('write output failed')
                    return

                self._log.warn('wrote %d bytes', ret)

                if ret < len(self._buf):
                    # partial write: del written part from buffer, try again
                    self._buf = self._buf[ret:]
                    continue

                # write was complete - empty buffer and return
                self._buf = ''
                return


            except OSError as e:

                if e.errno == errno.EAGAIN:
                    # pipe is full, retry later.  We don't want the child
                    # process to stall or fail on a full pty buffer, so we
                    # rather continue to pull the child and buffer here than
                    # to wait for the consumer to free the pipe buffer.
                    self._log.warn('pipe busy')
                    return

                elif e.errno == errno.EPIPE:

                    # pipe is broken - reopen a try again
                    # FIXME: how often do we want to retry?

                    self._log.warn('pipe broken')
                    try:
                        self._pout = os.open(self._fout,
                                             os.O_WRONLY | os.O_NONBLOCK, 0o600)
                        continue

                    except OSError as e1:
                        if e1.errno != errno.ENXIO:
                            raise

                        # can't recover right now - stop write attempts
                        return

                else:
                    # unexpected error - fail
                    raise

        # all data are written here


    # --------------------------------------------------------------------------
    def _fwd_pin(self, data):
        '''
        Similar helper for pty write - only that we don't attempt to recover: if
        the pty is gone, it means the child process is gone, which means we need
        to terminate anyway.
        '''

        while data:

            try:
                ret = os.write(self._pty, data)
                if ret:
                    data = data[ret:]

            except OSError as e:
                if e.errno != errno.EAGAIN:
                    raise


# ------------------------------------------------------------------------------

