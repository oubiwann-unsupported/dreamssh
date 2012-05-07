from twisted.conch.insults.insults import ServerProtocol
from twisted.conch.manhole_tap import *


connectionMadeOrig = ServerProtocol.connectionMade


def connectionMade(self, *args, **kwargs):
    connectionMadeOrig(self)
    self.write("This is your MOTD from the ServerProtocol monkeypatch!")


ServerProtocol.connectionMade = connectionMade
