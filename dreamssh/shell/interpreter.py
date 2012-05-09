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

    def updateNamespace(self, controller, namespace={}):
        pass


class DreamSSHInterpreter(ManholeInterpreter):
    """
    """
    # XXX namespace code needs to be better organized:
    #   * should the CommandAPI be in this module? 
    def updateNamespace(self, namespace={}):
        if not self.handler.commandAPI.appOrig:
            self.handler.commandAPI.appOrig = self.handler.namespace.get("app")
        namespace.update({
            "os": os,
            "sys": sys,
            "config": config,
            "pprint": pprint,
            "app": self.handler.commandAPI.getAppData,
            "banner": self.handler.commandAPI.banner,
            "info": self.handler.commandAPI.banner,
            "ls": self.handler.commandAPI.ls,
            "clear": self.handler.commandAPI.clear,
            "quit": self.handler.commandAPI.quit,
            "exit": self.handler.commandAPI.quit,
            })
        self.handler.namespace.update(namespace)
