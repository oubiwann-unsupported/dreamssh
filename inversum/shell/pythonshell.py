from pprint import pprint

from twisted.conch import manhole_ssh

from inversum import config
from inversum import exceptions
from inversum.shell import base


class CommandAPI(object):

    def __init__(self):
        self.namespace = None

    def setNamespace(self, namespace):
        self.namespace = namespace

    def ls(self):
        """
        List the objects in the current namespace, in alphabetical order.
        """
        keys = sorted(self.namespace.keys())
        pprint(keys)

    def banner(self):
        """
        Display the login banner and associated help or info.
        """
        print config.ssh.banner


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

    def __init__(self, namespace):
        self.sessionFactory.namespace = namespace
