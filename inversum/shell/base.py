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

    #def initializeScreen(self):
    def connectionMade(self, *args, **kwargs):
        #manhole.ColoredManhole.initializeScreen(self)
        manhole.ColoredManhole.connectionMade(self, *args, **kwargs)
        self.terminal.write(self.commandAPI.banner())
        self.updateNamespace()
        #self.namespace.update({'write': self.terminal.write})

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


class TerminalSession(manhole_ssh.TerminalSession):
    """
    """
    def windowChanged(self, coords):
        log.msg("New coordinates: %s" % str(coords))


class SessionForTerminalUser(object):
    """
    """
    def __init__(self, avatar):
        self.avatar = avatar
