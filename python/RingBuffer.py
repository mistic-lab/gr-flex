"""
A 1D ring buffer using numpy arrays
"""
from threading import RLock
import numpy as np

class RingBuffer(object):
    """
    A 1D ring buffer using numpy arrays
    """

    class Empty(Exception):
        """
        The RingBuffer.Empty Exception thrown when a read is issued on an empty buffer
        """
        pass

    class Full(Exception):
        """
        The RingBuffer.Full Exception thrown when a write is issued on a full buffer
        """
        pass

    def __init__(self, length=0):
        self.data = np.zeros(length, dtype='f')
        self.__size_used = 0
        self.read_index = 0
        self.index = 0
        self.__lock = RLock()

    @property
    def size_total(self):
        """ Gets the size of the entire buffer"""
        return self.data.size

    @property
    def size_remaining(self):
        """ Gets the size of the unused buffer space """
        with self.__lock:
            return self.size_total - self.size_used

    @property
    def size_used(self):
        """ Gets the current amount of the buffer that is used but unread """
        with self.__lock:
            return self.__size_used

    @property
    def is_empty(self):
        """ Gets whether or not thxe buffer is currently empty """
        with self.__lock:
            return self.__size_used == 0

    def add(self, items):
        """adds data items to ring buffer"""
        items_size = 0
        if isinstance(items, list):
            items_size = len(items)
        elif isinstance(items, np.ndarray):
            items_size = items.size

        with self.__lock:
            if self.size_remaining == 0:
                raise RingBuffer.Full

            items_index = (self.index + np.arange(items_size)) % self.data.size
            self.data[items_index] = items
            self.index = items_index[-1] + 1
            self.__size_used += items_size

    def get(self, number):
        """Returns the first-in-first-out data in the ring buffer"""
        with self.__lock:
            if self.is_empty:
                raise RingBuffer.Empty

            # if someone requests more data than in the buffer, just
            # give them the rest of the buffer
            number = min(number, self.size_used)

            out = np.roll(self.data, self.read_index)[0:number]
            self.__size_used -= number
            self.read_index += number
            return out
