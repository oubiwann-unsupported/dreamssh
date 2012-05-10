import os
from pprint import pprint
import sys

from twisted.conch import manhole, manhole_ssh
from twisted.python import log

from dreamssh import config


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
        termProto.terminal.write("\r\n" + config.ssh.banner + "\r\n")
        termProto.terminal.write(termProto.ps[termProto.pn])


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
