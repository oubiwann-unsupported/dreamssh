import os
from pprint import pprint
import sys

from twisted.conch import manhole_ssh
from twisted.conch.manhole import ManholeInterpreter

from dreamssh import config
from dreamssh import exceptions
from dreamssh.shell import base


class CommandAPI(object):

    def __init__(self):
        self.namespace = None
        self.terminal = None
        self.appData = None
        self.appOrig = None

    def setNamespace(self, namespace):
        self.namespace = namespace

    def setTerminal(self, terminal):
        self.terminal = terminal

    def setAppData(self):
        if not self.namespace:
            return
        if not self.appData:
            self.appData = {
                "servicecollection": self.appOrig._adapterCache.get(
                    "twisted.application.service.IServiceCollection"),
                "multiservice": self.appOrig._adapterCache.get(
                    "twisted.application.service.IService"),
                "process": self.appOrig._adapterCache.get(
                    "twisted.application.service.IProcess"),
                }

    def getAppData(self):
        return pprint(self.appData)

    def ls(self):
        """
        List the objects in the current namespace, in alphabetical order.
        """
        width = max([len(x) for x in self.namespace.keys()])
        for key, value in sorted(self.namespace.items()):
            info = ""
            if (isinstance(value, dict) or 
                isinstance(value, list) or key == "services"):
                info = "data"
            elif type(value).__name__ == "module":
                info = value.__name__
            elif type(value).__name__ == "function":
                info = "%s.%s" % (value.__module__, value.__name__)
            elif type(value).__name__ == "instance":
                info = "%s.%s" % (value.__module__, value.__class__.__name__)
            else:
                info = "%s.%s.%s" % (
                    value.im_class.__module__, value.im_class.__name__, key)
            print "\t%s - %s" % (key.ljust(width), info)

    def banner(self):
        """
        Display the login banner and associated help or info.
        """
        print config.ssh.banner

    def clear(self):
        self.terminal.reset()

    def quit(self):
        self.terminal.loseConnection()


class PythonSessionTransport(base.TerminalSessionTransport):

    def getHelpHint(self):
        return ("Type 'ls()' or 'dir()' to see the objects in the "
                "current namespace.")


class PythonTerminalSession(base.ExecutingTerminalSession):
    """
    """
    transportFactory = PythonSessionTransport

    def _processShellCommand(self, cmd, namespace):
        try:
            eval(cmd, namespace)
        except NameError:
            command = cmd.split("(")[0]
            msg = "Command '%s' not found in namespace!" % command
            raise exceptions.IllegalAPICommand(msg)


class PythonTerminalRealm(base.ExecutingTerminalRealm):
    """
    """
    sessionFactory = PythonTerminalSession
    transportFactory = PythonSessionTransport

    def __init__(self, namespace):
        base.ExecutingTerminalRealm.__init__(self, namespace)

        def getManhole(serverProtocol):
            return PythonManhole(CommandAPI(), namespace)

        self.chainedProtocolFactory.protocolFactory = getManhole


class PythonInterpreter(ManholeInterpreter):
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


class PythonManhole(base.MOTDColoredManhole):
    """
    """
    def setInterpreter(self, klass=None, namespace={}):
        if namespace:
            self.updateNamespace(namespace)
        else:
            namespace = self.namespace
        self.interpreter = PythonInterpreter(self, locals=namespace)

    def updateNamespace(self, namespace={}):
        self.interpreter.updateNamespace(namespace)
        self.commandAPI.setNamespace(self.namespace)
        self.commandAPI.setTerminal(self.terminal)
        self.commandAPI.setAppData()