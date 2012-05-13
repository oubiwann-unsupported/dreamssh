import os

from twisted.conch.ssh.keys import Key

from dreamssh import config
from dreamssh.apps import exceptions


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
