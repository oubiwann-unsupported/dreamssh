import os
from pprint import pprint
import sys

from twisted.conch import manhole, manhole_ssh
from twisted.python import log

from dreamssh.apps import registry


config = registry.getConfig()


def renderBanner(help=""):
    return config.ssh.banner.replace("{{HELP}}", help)


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

    def setInterpreter(self, namespace={}):
        raise NotImplementedError()

    def updateNamespace(self, namespace={}):
        raise NotImplementedError()


class TerminalSessionTransport(manhole_ssh.TerminalSessionTransport):
    """
    """
    def __init__(self, proto, chainedProtocol, avatar, width, height):
        manhole_ssh.TerminalSessionTransport.__init__(
            self, proto, chainedProtocol, avatar, width, height)
        self.writeMOTD()

    def writeMOTD(self):
        termProto = self.chainedProtocol.terminalProtocol
        banner = renderBanner(help=self.getHelpHint())
        termProto.terminal.write("\r\n" + banner + "\r\n")
        termProto.terminal.write(termProto.ps[termProto.pn])

    def getHelpHint(self):
        raise NotImplementedError()


class TerminalSession(manhole_ssh.TerminalSession):
    """
    """
    transportFactory = TerminalSessionTransport

    def windowChanged(self, coords):
        log.msg("New coordinates: %s" % str(coords))


class ExecutingTerminalSession(TerminalSession):
    """
    """
    def _processShellCommand(self, cmd, namespace):
        raise NotImplementedError()

    def execCommand(self, proto, cmd):
        avatar = proto.session.avatar
        conn = avatar.conn
        namespace = proto.session.session.namespace
        if cmd.startswith("scp"):
            exceptions.UnsupportedSubsystemError("scp is not supported")
        else:
            self._processShellCommand(cmd, namespace)
            conn.transport.loseConnection()


class ExecutingTerminalRealm(manhole_ssh.TerminalRealm):
    """
    """
    sessionFactory = ExecutingTerminalSession
    transportFactory = TerminalSessionTransport

    def __init__(self, namespace):
        manhole_ssh.TerminalRealm.__init__(self)
        self.sessionFactory.namespace = namespace
