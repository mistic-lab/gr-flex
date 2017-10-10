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
            out_sig=[numpy.float])
        
        self.recievedDataQueue = Queue.Queue()

        daxCh = 1
        print("FlexSource::GetOrCreatePanAdapter")
        pan = FlexApi.radio.GetOrCreatePanadapterSync(0,0) 
        pan.DAXIQChannel = daxCh
        print("FlexSource::CreatingIQStream")
        iq = FlexApi.radio.CreateIQStreamSync(daxCh)
        iq.DataReady += self.iq_data_received

    def iq_data_received(self,iqStream,data):
        print "Received {0} values".format(len(data))
        self.recievedDataQueue.put(data[:])
   
    def work(self, input_items, output_items):
        out = output_items[0]
        out[:] = self.recievedDataQueue.get()
        return len(output_items[0])

