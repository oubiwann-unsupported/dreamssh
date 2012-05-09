import os
from pprint import pprint
import sys

from twisted.conch import manhole, manhole_ssh
from twisted.python import log

from dreamssh import config
from dreamssh.shell.interpreter import DreamSSHInterpreter


class MOTDColoredManhole(manhole.ColoredManhole):
    """
    """
    ps = (":>> ", "... ")
    def __init__(self, commandAPI, *args, **kwargs):
        manhole.ColoredManhole.__init__(self, *args, **kwargs)
        self.commandAPI = commandAPI

    def connectionMade(self, *args, **kwargs):
        manhole.ColoredManhole.connectionMade(self, *args, **kwargs)
        # XXX how can we make this dynamic, based on options passed to twistd?
        self.setInterpreter()
        self.updateNamespace()

    def _getService(self, type="ssh"):
        if type == "ssh":
            return self.namespace["services"].getServiceNamed(
                config.ssh.servicename)

    def getSSHService(self):
        return self._getService(type="ssh")

    def setInterpreter(self, klass=None, namespace={}):
        if namespace:
            self.updateNamespace(namespace)
        else:
            namespace = self.namespace
        if not klass:
            klass = DreamSSHInterpreter
            #from dreamssh.shell.interpreter import EchoInterpreter
            #klass = EchoInterpreter
        self.interpreter = klass(self, locals=namespace)

    def updateNamespace(self, namespace={}):
        self.interpreter.updateNamespace(namespace)
        self.commandAPI.setNamespace(self.namespace)
        self.commandAPI.setTerminal(self.terminal)
        self.commandAPI.setAppData()


class TerminalSessionTransport(manhole_ssh.TerminalSessionTransport):
    """
    """
    def __init__(self, proto, chainedProtocol, avatar, width, height):
        manhole_ssh.TerminalSessionTransport.__init__(
            self, proto, chainedProtocol, avatar, width, height)
        self.writeMOTD()

    def writeMOTD(self):
        termProto = self.chainedProtocol.terminalProtocol
        termProto.terminal.write("\r\n" + config.ssh.banner + "\r\n")
        termProto.terminal.write(termProto.ps[termProto.pn])


class TerminalSession(manhole_ssh.TerminalSession):
    """
    """
    transportFactory = TerminalSessionTransport

    def windowChanged(self, coords):
        log.msg("New coordinates: %s" % str(coords))


class SessionForTerminalUser(object):
    """
    """
    def __init__(self, avatar):
        self.avatar = avatar
