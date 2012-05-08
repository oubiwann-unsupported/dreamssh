from twisted.conch.insults.insults import ServerProtocol
from twisted.conch.manhole import Manhole
from twisted.conch.manhole_tap import *
from twisted.conch.recvline import RecvLine


connectionMadeOrig = Manhole.connectionMade


class Interpreter(object):
    """
    A simple interpreter that demonstrate where one can plug in any
    command-parsing shell.
    """
    def __init__(self, handler, filename="<console>"):
        self.handler = handler
        self.filename = filename
        self.buffer = []

    def resetBuffer(self):
        self.buffer = []

    def push(self, line):
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        more = self.runsource(source, self.filename)
        if not more:
            self.resetBuffer()
        return more

    def runsource(self, input, filename):
        self.write("a = %s, b = %s" % (a, b))

    def write(self, data, async=False):
        self.handler.addOutput(data, async)


def connectionMade(self, *args, **kwargs):
    connectionMadeOrig(self)
    # As a general solution, a custom class can have a setInterpreter method,
    # override connectionMade, updall connectionMade, and then call its
    # setInterpreter method. This way, any subclass can provide it's own
    # interpreter.
    self.interpreter = Interpreter(self)


Manhole.connectionMade = connectionMade
