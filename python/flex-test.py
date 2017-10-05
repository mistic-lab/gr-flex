import socket
from struct import Struct,unpack_from
import ctypes
import array
from enum import Enum

UDP_PORT = 4991
BUFFER_SIZE = 150000

class VitaPacketType(Enum):
    IFData = 0
    IFDataWithStream = 1
    ExtData = 2
    ExtDataWithStream = 3
    IFContext = 4
    ExtContext = 5

class VitaTimeStampIntegerType(Enum):
    NONE = 0
    UTC = 1
    GPS = 2
    Other = 3

class VitaTimeStampFractionalType(Enum):
    NONE = 0
    SampleCount = 1
    RealTime = 2        # Picoseconds
    FreeRunning = 3

VitaClassId = Struct('>I H H')
SwappedInt = Struct('>I')

# Setup Socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind(("0.0.0.0",UDP_PORT))
rx_bytes = bytearray(BUFFER_SIZE)
rx_view = memoryview(rx_bytes)
# Listen forever
while True:
    nbytes = sock.recv_into(rx_view)
    offset = 0
    temp = SwappedInt.unpack_from(rx_view[offset:])[0]
    pkt_type = VitaPacketType(temp>>28)
    has_class_id = ((temp & 0x08000000) != 0)
    has_trailer = ((temp & 0x04000000) != 0)
    tsi = VitaTimeStampIntegerType((temp >> 22) & 0x03)
    tsf = VitaTimeStampFractionalType((temp >> 20) & 0x03)
    packet_count = ((temp >> 16) & 0x0F)
    packet_size = (temp & 0xFFFF)
    
    # Advance the offset past the header
    offset = offset+4
    
    if(pkt_type == VitaPacketType.IFDataWithStream or pkt_type == VitaPacketType.ExtDataWithStream):
         stream_id = SwappedInt.unpack_from(rx_view[offset:])[0]
         offset = offset +4

    if has_class_id:
        # TODO: Confirm that this actually works, don't need it right now so don't care
        class_id = VitaClassId.unpack_from(rx_view[offset:])
        class_id_oui = class_id[0]
        class_id_infoclasscode = class_id[1]
        class_id_packetclasscode = class_id[2]
        offset = offset + 8

    if has_trailer:
        # TODO: Implement If needed
        pass
    
    if(tsi != VitaTimeStampIntegerType.NONE):
        timestamp_int = SwappedInt.unpack_from(rx_view[offset:])[0]
        offset = offset + 4        

    if(tsf != VitaTimeStampFractionalType.NONE):
        timestamp_frac = unpack_from('>Q',rx_view[offset:])[0]
        offset = offset + 8

    vals = array.array('f',rx_bytes[offset:packet_size*4]) 


    print "received message:",vals 
