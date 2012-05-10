import os
from pprint import pprint
import sys

from twisted.conch import manhole_ssh
from twisted.conch.manhole import ManholeInterpreter

from dreamssh import config
from dreamssh import exceptions
from dreamssh.shell import base


class EchoTerminalSession(base.ExecutingTerminalSession):
    """
    """
    def _processShellCommand(self, cmd, namespace):
        pass


class EchoTerminalRealm(base.ExecutingTerminalRealm):
    """
    """
    sessionFactory = EchoTerminalSession

    def __init__(self, namespace):
        base.ExecutingTerminalRealm.__init__(self, namespace)

        def getManhole(serverProtocol):
            return EchoManhole(namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole


class EchoInterpreter(base.Interpreter):
    """
    A simple interpreter that demonstrate where one can plug in any
    command-parsing shell.
    """
    def runsource(self, input, filename):
        self.write("input = %s, filename = %s" % (input, filename))

    def updateNamespace(self, namespace={}):
        pass


class EchoManhole(base.MOTDColoredManhole):
    """
    """
    def __init__(self, namespace):
        base.MOTDColoredManhole.__init__(self, None, namespace)

    def setInterpreter(self, klass=None, namespace={}):
        if namespace:
            self.updateNamespace(namespace)
        else:
            namespace = self.namespace
        self.interpreter = EchoInterpreter(self, locals=namespace)

    def updateNamespace(self, namespace={}):
        self.interpreter.updateNamespace(namespace)
