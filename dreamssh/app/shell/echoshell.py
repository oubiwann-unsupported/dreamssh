from dreamssh.app.shell import base
from dreamssh.sdk import registry


config = registry.getConfig()


BANNER_HELP = "This shell has no commands; it simply returns what you type."


class EchoSessionTransport(base.TerminalSessionTransport):

    def getHelpHint(self):
        return BANNER_HELP


class EchoTerminalSession(base.ExecutingTerminalSession):
    """
    """
    transportFactory = EchoSessionTransport

    def _processShellCommand(self, cmd, namespace):
        pass


class EchoTerminalRealm(base.ExecutingTerminalRealm):
    """
    """
    sessionFactory = EchoTerminalSession
    transportFactory = EchoSessionTransport

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
