# Import CLR and add in mono assemblies
import clr
clr.AddReference("System")

flexLibDir = "../lib"
clr.AddReference("{0}/Vita".format(flexLibDir))
clr.AddReference("{0}/Flex.UiWpfFramework".format(flexLibDir))
clr.AddReference("{0}/Util".format(flexLibDir))
clr.AddReference("{0}/FlexLib".format(flexLibDir))

# Print the loaded assemblies
import System
domain = System.AppDomain.CurrentDomain
for item in domain.GetAssemblies():
    name = item.GetName()
    print("Loaded Assembly: {0}".format(name))

# Import CLR Types from mono assemblies
from Flex.Smoothlake.FlexLib import API

discovered_radio = None

def radio_added(radio):
    global discovered_radio
    discovered_radio = radio

API.RadioAdded += radio_added
API.ProgramName = "gnuradio"
API.Init()

# Here we wait until we have a connected radio
while discovered_radio is None:
    pass

radio = discovered_radio
print("Radio Discovered")
print("Model:\t\t\t{0}\r\nIp:\t\t\t{1}\r\nCommand Port (TCP):\t{2}\r\nData Port (UDP):\t{3}".format(radio.Model,radio.IP,radio.CommandPort,API.UDPPort))
print("Status:\t\t\t{0}".format(radio.Status))
print("Connecting...")
radio.Connect()

# Wait for the panAdapters
while len(radio.PanadapterList) == 0:
    pass

print("{0}".format(radio.Status))

daxChannel = 1
sampleRate = 192000

firstPan = radio.PanadapterList[0]
firstPan.DAXIQChannel = 0
firstPan.DAXIQChannel = daxChannel

iq = radio.CreateIQStreamSync(daxChannel)

def iq_data_received(iqStream,data):
    print "Received {0} floats".format(len(data))

iq.DataReady += iq_data_received
iq.SampleRate = sampleRate


# Wait forever for data to stream in
i = 0
while True:
    i = i+1
    if(i%100==0):
        print("Receiving: {0} Bytes/s".format(iq.BytesPerSecFromRadio))
    pass