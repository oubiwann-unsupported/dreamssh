from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase

from dreamssh.apps import const
from dreamssh.server.shell import base
from dreamssh.util import ssh as util


def portalFactory(interpreterType, namespace):
    if interpreterType == const.PYTHON:
        from dreamssh.server.shell import pythonshell
        realm = pythonshell.PythonTerminalRealm(namespace)
    elif interpreterType == const.ECHO:
        from dreamssh.server.shell import echoshell
        realm = echoshell.EchoTerminalRealm(namespace)
    return portal.Portal(realm)


def getShellFactory(interpreterType, **namespace):
    sshPortal = portalFactory(interpreterType, namespace)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory
