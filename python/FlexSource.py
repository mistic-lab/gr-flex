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
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
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
from gnuradio import gr
from flex import FlexApi
from RingBuffer import RingBuffer


class FlexSource(gr.sync_block):
    """
    The FlexSource block used for streaming and interacting with IQ Data
    Streams from the Flex Radio.
    """
    def __init__(self, center_freq=15000000, bandwidth=5000000,
                 rx_ant="ANT1", dax_iq_ch=1):
        gr.sync_block.__init__(self,
                               name="source",
                               in_sig=None,
                               out_sig=[numpy.complex64])
        self._center_freq = self.__hz_to_mhz(center_freq)
        self._bandwidth = self.__hz_to_mhz(bandwidth)
        self._rx_ant = rx_ant
        self._dax_iq_ch = dax_iq_ch
        print("FLEX:SOURCE:INIT")
        self.rx_buffer = None
        self.radio = None
        self.iq_stream = None
        self.pan_adapter = None

        self._debug = False

    def __hz_to_mhz(self, hz):
        mhz = hz / 1000000
        return mhz

    @property
    def center_freq(self):
        """
        Returns configured center frequency.
        """
        return self._center_freq

    def set_center_freq(self, center_freq):
        """
        Sets the center frequency of the underlying Panadapter

        Args:
            center_freq: the new center frequency
        """
        self._center_freq = self.__hz_to_mhz(center_freq)
        self.pan_adapter.CenterFreq = self._center_freq

    @property
    def bandwidth(self):
        """
        Returns configured bandwidth.
        """
        return self._bandwidth

    def set_bandwidth(self, bandwidth):
        """
        Sets the bandwidth of the underlying Panadapter

        Args:
            bandwidth: the new bandwidth
        """
        self._bandwidth = self.__hz_to_mhz(bandwidth)
        self.pan_adapter.Bandwidth = self._bandwidth

    @property
    def rx_ant(self):
        """
        Returns RX antenna in use.
        """
        return self._rx_ant

    def set_rx_ant(self, rx_ant):
        """
        Sets the RX antenna of the underlying Panadapter

        Args:
            rx_ant: the new RX antenna to use
        """
        self._rx_ant = self.rx_ant
        self.pan_adapter.RXAnt = self._rx_ant

    @property
    def dax_iq_ch(self):
        """
        Returns dax_iq_ch in use.
        """
        return self._dax_iq_ch

    def set_dax_iq_ch(self, dax_iq_ch):
        """
        Sets the DAX IQ channel of the underlying Panadapter

        Args:
            dax_iq_ch: the new DAX IQ channel to use
        """
        self._dax_iq_ch = self.dax_iq_ch
        self.pan_adapter.DAXIQChannel = self._dax_iq_ch

    def __iq_data_received(self, iq_stream, data):
        try:
            # Add the data to the receive buffer
            self.rx_buffer.add([float(num) for num in data])
        except RingBuffer.Full:
            # queue is full, drop packets I guess
            print("FLEX_SOURCE::Buffer Full, Packet Dropped")
        except Exception as err:
            print err

    def __property_changed(self, sender, args):
        """
        Prints out chosen property value with description each time it changes
        on the side of the panadapter.
        """
        if args.PropertyName == "Bandwidth":
            print("{0} Bandwidth Changed".format(
                self.pan_adapter.Bandwidth))

    def start(self):
        """
        Start method of GNU Block:
            - Gets active radio from api
            - Gets / creates Panadapter
            - Creates IQ Stream and begins listening
        """
        self.rx_buffer = RingBuffer(4096)  # 4 times the UDP payload size
        print("FlexSource::Starting...")
        self.radio = FlexApi().getRadio()

        # TODO: make this a parameter of the source block
        sample_rate = 192000  # Available in IQStream.cs

        self.pan_adapter = self.radio.GetOrCreatePanadapterSync(0, 0)

        if self._debug:
            self.pan_adapter.PropertyChanged += self.__property_changed

        print("FlexSource::Panadapter created (ch:{0}, center freq:{1} MHz, bandwidth:{2} MHz, RX antenna:{3} )".format(
            self.dax_iq_ch, self.center_freq, self.bandwidth, self.rx_ant))
        self.pan_adapter.DAXIQChannel = self.dax_iq_ch
        self.pan_adapter.CenterFreq = self.center_freq
        self.pan_adapter.Bandwidth = self.bandwidth
        self.pan_adapter.RXAnt = self.rx_ant

        print("FlexSource::CreatingIQStream")
        self.iq_stream = self.radio.CreateIQStreamSync(self.dax_iq_ch)
        self.iq_stream.DataReady += self.__iq_data_received
        self.iq_stream.SampleRate = sample_rate
        print("FlexSource::IQStreamCreated")
        return True

    def stop(self):
        """
        Cleans up the Flex resources being used by this block
        """
        print("FlexSource::Removing IQ & Pan Adapter")
        # Closes only this instance of pan_adapter
        self.pan_adapter.Close(True)
        self.iq_stream.Close()
        del self.rx_buffer
        print("FlexSource::Removed IQ & Panadapter, finished Queue")
        return True

    def work(self, input_items, output_items):
        """
        Since the Flex radio is pushing data to this computer via UDP,we push
        the data onto a queue and inside the work method (GNU-Radio's api) we
        pull the appropriate amount of data off of the queue and push it into
        the output buffer of the GNU Radio block
        """
        out = output_items[0]
        num_outputs = 0
        try:
            items = self.rx_buffer.get(out.size)
            items = items.astype(numpy.float32).view(numpy.complex64)
            num_outputs = items.size
            out[0:num_outputs] = items
        except RingBuffer.Empty:
            # Don't care, just an empty buffer
            pass

        return num_outputs
