import numpy as np
from threading import RLock

class RingBuffer():
    class Empty(Exception):
        pass
    
    class Full(Exception):
        pass  

    "A 1D ring buffer using numpy arrays"
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
        with self.__lock:
            return self.__size_used == 0

    def add(self, x):
        """adds data x to ring buffer"""
        x_size = 0
        if(type(x)is list):
            x_size = len(x)
        elif(type(x) is np.ndarray):
            x_size = x.size

        with self.__lock:
            if(self.size_remaining == 0):
                raise RingBuffer.Full      

            x_index = (self.index + np.arange(x_size)) % self.data.size
            self.data[x_index] = x
            self.index = x_index[-1] + 1
            self.__size_used += x_size

    def get(self,number):
        """Returns the first-in-first-out data in the ring buffer"""
        with self.__lock:
            if(self.is_empty):
                raise RingBuffer.Empty

            # if someone requests more data than in the buffer, just
            # give them the rest of the buffer
            number= min(number,self.size_used)

            out = np.roll(self.data,self.read_index)[0:number]
            self.__size_used -= number
            self.read_index += number
            return out