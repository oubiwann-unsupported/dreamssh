from twisted.conch.manhole import Manhole
from twisted.conch.manhole_tap import *


connectionMadeOrig = Manhole.connectionMade


def connectionMade(self, *args, **kwargs):
    connectionMadeOrig(self)
    self.terminal.write("This is your MOTD from the Manhole monkeypatch!")


Manhole.connectionMade = connectionMade
