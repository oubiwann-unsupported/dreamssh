import base64
from glob import glob
import os
from pprint import pprint
import sys

from zope import interface

from twisted.cred import checkers, portal
from twisted.conch import interfaces, manhole, manhole_ssh, unix
from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.conch.ssh import filetransfer, session
from twisted.conch.ssh.channel import SSHChannel
from twisted.conch.ssh.factory import SSHFactory
from twisted.conch.ssh.keys import Key
from twisted.python import components, failure, log

from inversum import config
from inversum import exceptions


def _getKey(path):
    if not os.path.exists(path):
        raise exceptions.MissingSSHServerKeysError()
    with open(path) as keyBlob:
        return Key.fromString(data=keyBlob.read())


def getPrivKey():
    privKeyPath = os.path.join(
        config.ssh.keydir, config.ssh.privkey)
    return _getKey(privKeyPath)


def getPubKey():
    pubKeyPath = os.path.join(
        config.ssh.keydir, config.ssh.pubkey)
    return _getKey(pubKeyPath)


class MOTDColoredManhole(manhole.ColoredManhole):
    """
    """
    ps = (":>> ", "... ")

    #def initializeScreen(self):
    def connectionMade(self, *args, **kwargs):
        #manhole.ColoredManhole.initializeScreen(self)
        manhole.ColoredManhole.connectionMade(self, *args, **kwargs)
        self.terminal.write(self.getMOTD())
        self.namespace.update({'clear': self.terminal.reset})
        #self.namespace.update({'write': self.terminal.write})

    def getMOTD(self):
        return config.ssh.banner or "Welcome to MOTDColoredManhole!"


class TerminalSession(manhole_ssh.TerminalSession):
    """
    """
    def windowChanged(self, coords):
        log.msg("New coordinates: %s" % str(coords))


class ExecutingTerminalSession(TerminalSession):
    """
    """
    def _processShellCommand(self, cmd, namespace):
        try:
            result = eval(cmd, namespace)
        except NameError:
            command = cmd.split("(")[0]
            msg = "Command '%s' not found in namespace!" % command
            raise exceptions.IllegalAPICommand(msg)

    def execCommand(self, proto, cmd):
        avatar = proto.session.avatar
        conn = avatar.conn
        namespace = updateNamespace(proto.session.session.namespace)
        if cmd.startswith("scp"):
            # XXX raise custom error
            pass
        else:
            self._processShellCommand(cmd, namespace)
            avatar.conn.transport.loseConnection()


class SessionForTerminalUser(object):
    """
    """

    def __init__(self, avatar):
        self.avatar = avatar


class ExecutingTerminalRealm(manhole_ssh.TerminalRealm):
    """
    """
    sessionFactory = ExecutingTerminalSession

    def __init__(self, namespace):
        self.sessionFactory.namespace = namespace


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


def updateNamespace(namespace):
    sshService = namespace["services"].getServiceNamed(
        config.ssh.servicename)
    commands = CommandAPI()
    namespace.update({
        "os": os,
        "sys": sys,
        "config": config,
        "pprint": pprint,
        "banner": commands.banner,
        "info": commands.banner,
        })
    commands.setNamespace(namespace)
    return namespace


def getShellFactory(**namespace):

    def getManhole(serverProtocol):
        return MOTDColoredManhole(updateNamespace(namespace))

    realm = ExecutingTerminalRealm(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    sshPortal = portal.Portal(realm)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': getPrivKey()}
    factory.publicKeys = {'ssh-rsa': getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory
