from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase

from dreamssh import const, util
from dreamssh.shell import base, pythonshell


def portalFactory(interpreterType, namespace):
    if interpreterType == const.PYTHON:

        def getManhole(serverProtocol):
            commandAPI = pythonshell.CommandAPI()
            return pythonshell.PythonManhole(commandAPI, namespace)

        realm = pythonshell.PythonTerminalRealm(namespace)
        realm.chainedProtocolFactory.protocolFactory = getManhole

    elif interpreterType == const.ECHO:
        pass
    return portal.Portal(realm)


def getShellFactory(interpreterType, **namespace):
    sshPortal = portalFactory(interpreterType, namespace)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory
