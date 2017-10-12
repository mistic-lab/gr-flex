from source import source
import numpy

s = source()
s.start()

i = []
o = [[0]*9000]

while True:
    s.work(i,o)

# def receive(iq_stream,data):
#     print("Received some bits")

#s.iq.DataReady += receive

i = 0
while True:
    i = i+1
    if(i%100==0):
        print("Receiving: {0} Bytes/s".format(s.iq.BytesPerSecFromRadio))
    pass


