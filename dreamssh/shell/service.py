from twisted.cred import portal
from twisted.conch import manhole_ssh
from twisted.conch.checkers import SSHPublicKeyDatabase

from dreamssh import util
from dreamssh.shell import base, pythonshell, gameshell


def getShellFactory(**namespace):

    def getManhole(serverProtocol):
        commandAPI = pythonshell.CommandAPI()
        return base.MOTDColoredManhole(commandAPI, namespace)

    realm = pythonshell.ExecutingTerminalRealm(namespace)
    realm.chainedProtocolFactory.protocolFactory = getManhole
    sshPortal = portal.Portal(realm)
    factory = manhole_ssh.ConchFactory(sshPortal)
    factory.privateKeys = {'ssh-rsa': util.getPrivKey()}
    factory.publicKeys = {'ssh-rsa': util.getPubKey()}
    factory.portal.registerChecker(SSHPublicKeyDatabase())
    return factory
