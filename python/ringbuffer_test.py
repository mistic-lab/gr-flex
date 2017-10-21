import sys
import logging
import threading
import time
import numpy as np
import unittest
from RingBuffer import RingBuffer

class RingBufferTests(unittest.TestCase):

    def assert_arrays(self,a1,a2,msg="Array's not equal"):
        self.assertTrue(a1.size==a2.size,"{0}: {1} != {2}".format(msg,a1,a2))
        self.assertTrue(np.array_equal(a1,a1),"{0}: {1} != {2}".format(msg,a1,a2))   

    # @property
    # def log(self):
    #     return self._log

    def setUp(self):
        # self._log = logging.getLogger("RingBuffer.Tests")
        self.sample_data = np.arange(10.0)
        self.ring_buffer = RingBuffer(10)

    def tearDown(self):
        del self.ring_buffer
    
    def test_size_total(self):
        self.assertEqual(self.ring_buffer.size_total,10,'total size incorrect')

    def test_size_used(self):
        d = [0,1,3]
        self.ring_buffer.add(d)
        self.assertEqual(self.ring_buffer.size_used,len(d),'used size incorrect')        
        self.ring_buffer.get(2)
        self.assertEqual(self.ring_buffer.size_used,1,'used size incorrect')   

    def test_size_used(self):
        d = [0,1,3]
        self.ring_buffer.add(d)
        self.assertEqual(self.ring_buffer.size_remaining,self.ring_buffer.size_total-len(d),'remaining size incorrect')        
        self.ring_buffer.get(2)
        self.assertEqual(self.ring_buffer.size_remaining,9,'remaining size incorrect')   
         
    def test_basic_get(self):
        self.ring_buffer.add(self.sample_data[0:5])
        data = self.ring_buffer.get(2)
        self.assert_arrays(data,self.sample_data[0:2])

    def test_second_get(self):
        self.ring_buffer.add(self.sample_data[0:5])
        data = self.ring_buffer.get(2)
        data = self.ring_buffer.get(2)
        self.assert_arrays(data,self.sample_data[3:5])        

    def test_read_all_data_when_number_is_larger_than_buffer(self):
        d  = self.sample_data[0:2]
        self.ring_buffer.add(d)
        g = self.ring_buffer.get(4)
        self.assert_arrays(d,g)
        self.assertEqual(self.ring_buffer.size_used,0)


    def test_throw_on_read_from_empty_buffer(self):
        self.ring_buffer.add(self.sample_data[0:2])
        self.ring_buffer.get(2)
        # Should throw exception if reading beyond buffer
        with self.assertRaises(RingBuffer.Empty):
            data = self.ring_buffer.get(2)
  
    def test_throw_on_write_to_full_buffer(self):
        # Should throw if buffer is full
        self.ring_buffer.add(self.sample_data)   # Fill buffer
        with self.assertRaises(RingBuffer.Full):
            self.ring_buffer.add([0,1])

        # once we get some items, we should be able to add
        self.ring_buffer.get(2)
        self.ring_buffer.add([0,1])

        # adding anything else should throw again
        with self.assertRaises(RingBuffer.Full):
            self.ring_buffer.add([4])

    def test_should_be_thread_safe(self):

        def write_thread(ring,w_buf):
            #print "Writing to ring buffer"
            for j in range(0,w_buf.size,2):
                ring.add(w_buf[j:j+2])
                #print "Write:Sleep for .1 sec"
                time.sleep(.1)
        
        def read_thread(ring,buf):
            #print "Reading from RingBuffer"
            for i in range(buf.size):
                buf[i] = ring.get(1)
                #print "Read:Sleep for .06 sec"
                time.sleep(0.06)

        write_buf = np.arange(10.0,20.0)
        # Write thread
        wt = threading.Thread(target=write_thread,args=(self.ring_buffer,write_buf))

        data = np.zeros(shape=10)
        rt = threading.Thread(target=read_thread,args=(self.ring_buffer,data))

        wt.start()
        time.sleep(0.01)
        rt.start()
        wt.join()
        rt.join()   
        self.assert_arrays(write_buf,data)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(RingBufferTests)
    unittest.TextTestRunner(verbosity=3).run(suite)

