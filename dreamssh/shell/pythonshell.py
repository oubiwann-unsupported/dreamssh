from pprint import pprint

from twisted.conch import manhole_ssh

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


class ExecutingTerminalSession(base.TerminalSession):
    """
    """
    def _processShellCommand(self, cmd, namespace):
        try:
            eval(cmd, namespace)
        except NameError:
            command = cmd.split("(")[0]
            msg = "Command '%s' not found in namespace!" % command
            raise exceptions.IllegalAPICommand(msg)

    def execCommand(self, proto, cmd):
        avatar = proto.session.avatar
        conn = avatar.conn
        namespace = proto.session.session.namespace
        if cmd.startswith("scp"):
            # XXX raise custom error
            pass
        else:
            self._processShellCommand(cmd, namespace)
            conn.transport.loseConnection()


class ExecutingTerminalRealm(manhole_ssh.TerminalRealm):
    """
    """
    sessionFactory = ExecutingTerminalSession
    transportFactory = base.TerminalSessionTransport

    def __init__(self, namespace):
        self.sessionFactory.namespace = namespace
