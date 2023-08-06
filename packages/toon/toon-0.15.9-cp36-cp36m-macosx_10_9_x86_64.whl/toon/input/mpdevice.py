import ctypes
import multiprocessing as mp
import os
from collections import namedtuple
from sys import platform

import numpy as np
from numpy.ctypeslib import as_ctypes_type
from psutil import pid_exists

from toon.input._tbprocess import Process
from toon.util import priority

ret = namedtuple('mpdata', ['time', 'data'])
noneret = ret(None, None)


def shared_to_numpy(mp_arr, dims):
    """Convert a :class:`multiprocessing.Array` to a numpy array.
    Helper function to allow use of a :class:`multiprocessing.Array` as a numpy array.
    Derived from the answer at:
    <https://stackoverflow.com/questions/7894791/use-numpy-array-in-shared-memory-for-multiprocessing>
    """
    return np.frombuffer(mp_arr, dtype=mp_arr._type_).reshape(dims)


class MpDevice(object):
    """Creates and manages a process for polling an input device."""

    def __init__(self, device, buffer_len=None, use_views=False):
        """Create a new MpDevice.

        Parameters
        ----------
        device: object (derived from toon.input.BaseDevice)
            Input device object.
        buffer_len: int, optional
            Overrides the device's sampling_frequency when specifing the size of the
            circular buffer.
        use_views: bool, optional
            Return views (False by default; faster, but more error-prone) or copy data returned by `read()`.
        """
        self.device = device
        self.buffer_len = buffer_len
        self._use_views = use_views
        self.process = None
        # For Macs, use spawn (interaction with OpenGL or ??)
        # Windows only does spawn
        if platform in ['darwin', 'win32']:
            mp.freeze_support()  # for Windows executable support
            try:
                mp.set_start_method('spawn')
            except (AttributeError, RuntimeError):
                pass  # already started a process, or on python2

        n_buffers = 2
        # make one lock per buffer
        self.shared_locks = [mp.Lock() for i in range(n_buffers)]
        self.remote_ready = mp.Event()  # signal to main process that remote is done setup
        self.kill_remote = mp.Event()  # signal to remote process to die
        self.current_buffer_index = mp.RawValue(ctypes.c_bool, 0)

        # figure out number of observations to save between reads
        nrow = 100  # default (100 Hz)
        # if we have a sampling_frequency, allocate 1s worth
        # should be enough wiggle room for 60Hz refresh rate
        if self.device.sampling_frequency:
            nrow = self.device.sampling_frequency
        if self.buffer_len:  # buffer_len overcomes all
            nrow = self.buffer_len
        nrow = int(max(nrow, 1))  # make sure we have at least one row

        # preallocate data
        # we have a double buffer sort of thing going on,
        # so we need two of everything
        self._data = []
        time_type = as_ctypes_type(type(self.device.clock()))
        for lck in self.shared_locks:
            # make mp version
            is_scalar = False
            if self.device.shape == (1,):
                new_dim = (nrow,)
                is_scalar = True
            else:
                new_dim = (nrow,) + self.device.shape
            flat_dim = int(np.product(new_dim))
            ctype = self.device.ctype
            # Structures get padding when passing through this,
            # so only run on non-Structures
            if isinstance(ctype, list):
                ctype = as_ctypes_type(ctype)
                globals()['struct'] = ctype
            elif not issubclass(ctype, ctypes.Structure):
                ctype = as_ctypes_type(ctype)
            mp_arr = mp.RawArray(ctype, flat_dim)
            np_arr = shared_to_numpy(mp_arr, new_dim)
            t_mp_arr = mp.RawArray(time_type, nrow)
            t_np_arr = shared_to_numpy(t_mp_arr, nrow)
            counter = mp.RawValue(ctypes.c_uint, 0)
            # generate local version
            local_arr = np.empty_like(np_arr)
            t_local_arr = np.empty_like(t_np_arr)
            if is_scalar:
                local_arr = np.squeeze(local_arr)
            # special case for buffer size of 1 and scalar data
            if local_arr.shape == ():
                local_arr.shape = (1,)
            data_pack = {'mp_data': mp_arr, 'np_data': np_arr,
                         'mp_time': t_mp_arr, 'np_time': t_np_arr,
                         'counter': counter, 'lock': lck}
            self._data.append(data_pack)

        # make local versions to copy the data into
        self._local_arr = local_arr
        self._t_local_arr = t_local_arr
        self.device.local = True

    def start(self):
        """Start polling from the device on the child process.
        Allocates all resources and creates the child process.

        Notes
        -----
        Prefer using as a context manager over explicitly starting and stopping.

        Raises
        ------
        Will raise an exception if something goes wrong during instantiation
        of the device.
        """
        if not self.device.local:
            raise RuntimeError('MpDevice is already started.')
        self.process = Process(target=remote,
                               kwargs={'dev': self.device,
                                       'data': self._data,
                                       'remote_ready': self.remote_ready,
                                       'kill_remote': self.kill_remote,
                                       'parent_pid': os.getpid(),
                                       'current_buffer_index': self.current_buffer_index})

        self.process.daemon = True
        self.process.start()
        self.check_error()
        self.remote_ready.wait()  # block until child process is ready
        self.device.local = False  # try to prevent local access to the device

    def read(self):
        """Retrieve all observations that have occurred since the last read.
        Notes
        -----
        The data is stored in a circular buffer, which means that if the number
        of observations since the last read exceeds the preallocated data, the oldest
        data will be overwritten in favor of the newest. If this behavior is undesirable,
        either bump the sampling_frequency of the Device or the buffer_len of the MpDevice
        up to an adequate number, depending on the sampling rate of the device and how
        often you expect to call read().
        We copy data by default. If `use_views` is set to True upon initialization,
        then *views* are returned, which is faster (but more error prone).

        Returns
        -------
        Named tuple (time, data), or None if there is no data.

        Raises
        ------
        May raise an exception if one has occurred on the child process since the last read.
        """
        self.check_error()
        # get the current buffer (either 0 or 1)
        current_buffer_index = self.current_buffer_index.value
        # this might block, if the remote is currently writing data
        current_data = self._data[current_buffer_index]
        with current_data['lock']:
            local_count = current_data['counter'].value
            if local_count > 0:
                current_data['counter'].value = 0  # start writing from the top of the array
                t_out = self._t_local_arr[:local_count]
                data_out = self._local_arr[:local_count]
                data_out[:] = current_data['np_data'][:local_count]
                t_out[:] = current_data['np_time'][:local_count]
            else:
                return None
        # return time, data views (fast)
        if self._use_views:
            return ret(t_out, data_out)
        # otherwise, return copies
        return ret(np.copy(t_out), np.copy(data_out))

    def clear(self):
        """Discard all pending observations."""
        self.check_error()
        current_buffer_index = self.current_buffer_index.value
        current_data = self._data[current_buffer_index]
        with current_data['lock']:
            current_data['counter'].value = 0

    def check_error(self):
        """See if any exceptions have occurred on the child process, or whether
        the device was already closed.
        """
        if self.process:
            if not self.process.is_alive():
                if self.process.exception:
                    err, traceback = self.process.exception
                    print(traceback)
                    raise err
                else:
                    raise RuntimeError('MpDevice is closed.')
        else:
            raise RuntimeError('MpDevice has not been started yet.')

    def stop(self):
        """Stop reading from the device and kill the child process.
        Notes
        -----
        Prefer using as a context manager over explicitly starting and stopping.
        """
        self.kill_remote.set()
        self.process.join(timeout=1)
        self.device.local = True
        self.kill_remote.clear()
        self.remote_ready.clear()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()


def process_data(shared_time, shared_data, local_time, local_data, shared_counter, is_struct):
    next_index = shared_counter.value
    if is_struct:
        # np.ctypeslib.as_array is ~30x slower?
        local_data = np.frombuffer(local_data, dtype=shared_data.dtype)
    if next_index < shared_time.shape[0]:
        shared_time[next_index] = local_time
        shared_data[next_index] = local_data
        shared_counter.value += 1
    else:  # ring buffer ish, see benchmarks https://github.com/aforren1/toon/issues/77
        shared_time[:-1] = shared_time[1:]
        shared_time[-1] = local_time
        shared_data[:-1] = shared_data[1:]
        shared_data[-1] = local_data


def remote(dev, data, remote_ready, kill_remote, parent_pid, current_buffer_index):
    # from timeit import default_timer
    for d in data:
        # need to re-generate connection between mp and np arrays
        dims = d['np_data'].shape
        d['np_data'] = shared_to_numpy(d['mp_data'], dims)
        d['np_time'] = shared_to_numpy(d['mp_time'], dims[0])
        is_struct = d['np_data'].dtype.type == np.void
    try:
        priority(1)  # high priority (non-realtime, though) and disables gc
        with dev:
            remote_ready.set()  # signal all set to the parent process
            while not kill_remote.is_set() and pid_exists(parent_pid):
                # either a (time, data) tuple or list of (time, data) tuples
                # or None if nothing
                device_dat = dev.read()
                # t0 = default_timer()
                if device_dat is None:
                    continue  # next read
                buffer_index = current_buffer_index.value
                # lock magicks
                # test whether the current buffer is accessible
                current_data = data[buffer_index]
                lck = current_data['lock']
                success = lck.acquire(block=False)
                if not success:
                    current_buffer_index.value = not current_buffer_index.value
                    buffer_index = not buffer_index
                    current_data = data[buffer_index]
                    lck = current_data['lock']
                    # manual lock handling
                    lck.acquire()
                try:
                    shared_time = current_data['np_time']
                    shared_data = current_data['np_data']
                    shared_counter = current_data['counter']
                    if isinstance(device_dat, list):
                        for dat in device_dat:
                            process_data(shared_time, shared_data,
                                         dat[0], dat[1], shared_counter, is_struct)
                    else:
                        process_data(shared_time, shared_data,
                                     device_dat[0], device_dat[1], shared_counter, is_struct)
                finally:
                    lck.release()
                # print(default_timer() - t0)

    finally:
        priority(0)
        remote_ready.set()
