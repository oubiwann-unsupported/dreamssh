from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase

from dreamssh import const, util
from dreamssh.shell import base


def portalFactory(interpreterType, namespace):
    if interpreterType == const.PYTHON:
        from dreamssh.shell import pythonshell
        realm = pythonshell.PythonTerminalRealm(namespace)
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
