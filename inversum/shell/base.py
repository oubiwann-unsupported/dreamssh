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
        self._appData = None

    #def initializeScreen(self):
    def connectionMade(self, *args, **kwargs):
        #manhole.ColoredManhole.initializeScreen(self)
        manhole.ColoredManhole.connectionMade(self, *args, **kwargs)
        self.terminal.write(self.getMOTD())
        self.updateNamespace()
        #self.namespace.update({'write': self.terminal.write})

    def _getService(self, type="ssh"):
        if type == "ssh":
            return self.namespace["services"].getServiceNamed(
                config.ssh.servicename)

    def getSSHService(self):
        return self._getService(type="ssh")

    def setAppData(self):
        if not self._appData:
            app = self.namespace.get("app")
            self._appData = {
                "servicecollection": app._adapterCache.get(
                    "twisted.application.service.IServiceCollection"),
                "multiservice": app._adapterCache.get(
                    "twisted.application.service.IService"),
                "process": app._adapterCache.get(
                    "twisted.application.service.IProcess"),
                }

    def getAppData(self):
        return pprint(self._appData)

    def updateNamespace(self, namespace={}):
        clear = lambda: "undefined"
        quit = lambda: "undefined"
        if self.terminal:
            clear = self.terminal.reset
            quit = self.terminal.loseConnection
        app = self.namespace.get("app")
        if not self._appData:
            self.setAppData()
        namespace.update({
            "app": self.getAppData,
            "os": os,
            "sys": sys,
            "config": config,
            "pprint": pprint,
            "banner": self.commandAPI.banner,
            "info": self.commandAPI.banner,
            "ls": self.commandAPI.ls,
            "clear": clear,
            "quit": quit,
            })
        self.commandAPI.setNamespace(namespace)
        self.namespace.update(namespace)

    def getMOTD(self):
        return config.ssh.banner or "Welcome to MOTDColoredManhole!"


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



