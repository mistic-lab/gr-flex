import clr
from os import path

# Get the current directory
scriptDir = path.dirname(path.realpath(__file__))
flexLibDir = "{0}/FlexlibMono".format(scriptDir)
print("gr-flex::directory: \t\t\t{0}".format(scriptDir))
print("gr-flex::FlexLibMono_Directory: \t{0}".format(flexLibDir))

# Import FlexlibMono assemblies
clr.AddReference("System")
clr.AddReference("{0}/Vita".format(flexLibDir))
clr.AddReference("{0}/Util".format(flexLibDir))
clr.AddReference("{0}/FlexLib".format(flexLibDir))
clr.AddReference("{0}/Flex.UiWpfFramework.dll".format(flexLibDir))

# Print the loaded assemblies
import System
domain = System.AppDomain.CurrentDomain
for item in domain.GetAssemblies():
    name = item.GetName()
    print("Loaded Assembly: {0}".format(name))

# Import the API
from Flex.Smoothlake.FlexLib import API

class FlexApi: 
    radio = None

    def __print_radio_info(self,radio):
        print("Radio Discovered")
        print("Model:\t\t\t{0}\r\nIp:\t\t\t{1}\r\nCommand Port (TCP):\t{2}\r\nData Port (UDP):\t{3}".format(radio.Model,radio.IP,radio.CommandPort,API.UDPPort))
        print("Status:\t\t\t{0}".format(radio.Status))

    def __radio_added(self,foundRadio):
        FlexApi.radio = foundRadio

    def __initRadio(self):
        print("Initializing FlexLib API...\t")
        API.RadioAdded += self.__radio_added
        API.ProgramName = "gnuradio"
        API.Init()
        print("OK")

        print("Discovering Radios...\t\t")
        # Here we wait until we have a connected radio
        while FlexApi.radio is None:
            pass
        
        # Remove our event handler
        API.RadioAdded -= self.__radio_added

        self.__print_radio_info(FlexApi.radio)
        print("Connecting...")
        FlexApi.radio.Connect()

    def getRadio(self):
        if(FlexApi.radio is None):
            self.__initRadio()
        return FlexApi.radio



 



