import os
from pprint import pprint
import sys

from twisted.conch import manhole, manhole_ssh
from twisted.python import log

from inversum import config


class MOTDColoredManhole(manhole.ColoredManhole):
    """
    """
    ps = (":>> ", "... ")
    def __init__(self, commandAPI, *args, **kwargs):
        manhole.ColoredManhole.__init__(self, *args, **kwargs)
        self.commandAPI = commandAPI

    def connectionMade(self, *args, **kwargs):
        manhole.ColoredManhole.connectionMade(self, *args, **kwargs)
        self.updateNamespace()

    def _getService(self, type="ssh"):
        if type == "ssh":
            return self.namespace["services"].getServiceNamed(
                config.ssh.servicename)

    def getSSHService(self):
        return self._getService(type="ssh")

    def updateNamespace(self, namespace={}):
        if not self.commandAPI.appOrig:
            self.commandAPI.appOrig = self.namespace.get("app")
        namespace.update({
            "os": os,
            "sys": sys,
            "config": config,
            "pprint": pprint,
            "app": self.commandAPI.getAppData,
            "banner": self.commandAPI.banner,
            "info": self.commandAPI.banner,
            "ls": self.commandAPI.ls,
            "clear": self.commandAPI.clear,
            "quit": self.commandAPI.quit,
            })
        self.namespace.update(namespace)
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
