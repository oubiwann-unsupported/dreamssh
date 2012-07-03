import base64, binascii

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
    def getAuthorizedKeysFiles(self, credentials):
        if config.ssh.usesystemkeys:
            return SSHPublicKeyDatabase.getAuthorizedKeysFiles(
                self, credentials)
        return [FilePath(
            config.ssh.userauthkeys.replace("{{USER}}", credentials.username))]

    def checkKey(self, credentials):
        if config.ssh.usesystemkeys:
            return SSHPublicKeyDatabase.checkKey(
                self, credentials)
        for filePath in self.getAuthorizedKeysFiles(credentials):
            if not filePath.exists():
                continue
            lines = filePath.open()
            for line in lines:
                lineData = line.split()
                if len(lineData) < 2:
                    continue
                try:
                    if base64.decodestring(lineData[1]) == credentials.blob:
                        return True
                except binascii.Error:
                    continue
        return False
