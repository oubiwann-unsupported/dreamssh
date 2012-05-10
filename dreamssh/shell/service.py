from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase

from dreamssh import util
from dreamssh.shell import base, pythonshell


def realmFactory(interpreterType, namespace):
    if interpreterType == base.PYTHON:
        pass
    elif interpreterType == base.ECHO:
        pass


def getShellFactory(interpreterType, **namespace):

    def getManhole(serverProtocol):
        commandAPI = pythonshell.CommandAPI()
        return pythonshell.PythonManhole(commandAPI, namespace)

    realm = pythonshell.PythonTerminalRealm(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    sshPortal = portal.Portal(realm)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory
