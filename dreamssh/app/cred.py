from twisted.conch.checkers import SSHPublicKeyDatabase
from twisted.python.filepath import FilePath

from dreamssh.sdk import registry


config = registry.getConfig()


class PublicKeyDatabase(SSHPublicKeyDatabase):
    """
    A cred checker for SSH keys in arbitrary locations.

    This class provides similar functionality as its parent class, with the
    additional functionality of being able to use directories other than (or in
    addition to) the default provided by SSHPublicKeyDatabase (~/.ssh).
    """
    def getAuthorizedKeysFiles(self, credentials, useSystem=False):
        if useSystem:
            return SSHPublicKeyDatabase.getAuthorizedKeysFiles(
                self, credentials)
        return [FilePath(config.ssh.userauthkeys % credentials.username)]
