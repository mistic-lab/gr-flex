#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MIT License
# 
# Copyright (c) 2017 Colter McQuay
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
import numpy
import Queue
from array import array
from gnuradio import gr
from flex import FlexApi

class source(gr.sync_block):
    """
    docstring for block source
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="source",
            in_sig=None,
            out_sig=[numpy.float32])     
#        self.set_output_multiple(1024)

    def iq_data_received(self,iqStream,data):
        for num in data:
            self.receivedDataQueue.put(float(num))
   
    def start(self):
        print("FlexSource::Starting...")
        self.receivedDataQueue = Queue.Queue()
        self.radio = FlexApi().getRadio()
        daxCh = 1
        print("FlexSource::GetOrCreatePanAdapter")
        pans = self.radio.WaitForPanadaptersSync()
        # Close any panAdapters currently setup
        for p in pans:
            p.Close(True)
        pan = self.radio.GetOrCreatePanadapterSync(0,0) 
        pan.DAXIQChannel = daxCh
        pan.CenterFreq = 14.272
        print("FlexSource::CreatingIQStream")
        self.iq = self.radio.CreateIQStreamSync(daxCh)
        self.iq.DataReady += self.iq_data_received
        self.iq.SampleRate = 192000        
        print("FlexSource::IQStreamCreated")
        return True

    def stop(self):
        print("FlexSource::Closing Radio")
        self.radio.Close()
        return True

    def work(self,input_items, output_items):
        out = output_items[0]
        try:
            for i in range(0,out.size-1):
                num = self.receivedDataQueue.get_nowait()
                out[i]= num
        except Queue.Empty:
            # Happens when the queue is empty, no prob
            pass
        finally:
            num_items = i

        return num_items
        
        

