from pprint import pprint
import os
import sys

from twisted.conch.manhole import Manhole, ManholeInterpreter

from dreamssh import config


class Interpreter(object):
    """
    A base class for interpreters.
    """
    def __init__(self, handler, locals=None, filename="<console>"):
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
        raise NotImplementedError()

    def write(self, data, async=False):
        self.handler.addOutput(data, async)

    def updateNamespace(self, namespace={}):
        raise NotImplementedError()


class EchoInterpreter(Interpreter):
    """
    A simple interpreter that demonstrate where one can plug in any
    command-parsing shell.
    """
    def runsource(self, input, filename):
        self.write("input = %s, filename = %s" % (input, filename))

    def updateNamespace(self, namespace={}):
        pass
