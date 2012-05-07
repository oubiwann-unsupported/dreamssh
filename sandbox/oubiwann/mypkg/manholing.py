from twisted.conch.insults.insults import ServerProtocol
from twisted.conch.manhole import Manhole
from twisted.conch.manhole_tap import *
from twisted.conch.recvline import RecvLine


connectionMadeOrig = Manhole.connectionMade


def connectionMade(self, *args, **kwargs):
    connectionMadeOrig(self)
    self.terminal.write("This is your MOTD from the Manhole monkeypatch!")


ServerProtocol.reset = lambda self: None
RecvLine.initializeScreen = lambda self: None # <-- this is the cuplrit!
# In order to get a MOTD, you need to override
# manhole_ssh.TerminalSession.openShell, and do the MOTD after the upcall to
# openShell.
RecvLine.terminalSize = lambda self, w, h: None
Manhole.connectionMade = connectionMade
