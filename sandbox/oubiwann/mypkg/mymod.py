from twisted.conch.insults.insults import (
    TerminalProtocol, ClientProtocol, ServerProtocol)
from twisted.conch.manhole_tap import *


def printMOTD(self):
    #self.terminal.write("This is your MOTD!")
    self.write("This is your MOTD!")

connectionMadeOrig = ServerProtocol.connectionMade
    
def connectionMade(self, *args, **kwargs):
    connectionMadeOrig(self)
    self.printMOTD()

ServerProtocol.printMOTD = printMOTD
ServerProtocol.connectionMade = connectionMade
