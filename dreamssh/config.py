from ConfigParser import SafeConfigParser
import os

from zope.interface import moduleProvides

from dreamssh import meta
from dreamssh.sdk import interfaces


moduleProvides(interfaces.IConfig)


class Config(object):
    pass


# Main
main = Config()
main.config = Config()
main.config.userdir = os.path.expanduser("~/.%s" % meta.library_name)
main.config.localfile = "config.ini"
main.config.userfile = "%s/%s" % (main.config.userdir, main.config.localfile)

# Internal SSH Server
ssh = Config()
ssh.servicename = meta.description
ssh.port = 2222
ssh.pidfile = "twistd.pid"
ssh.username = "root"
ssh.keydir = os.path.join(main.config.userdir, "ssh")
ssh.privkey = "id_rsa"
ssh.pubkey = "id_rsa.pub"
ssh.localdir = "~/.ssh"
ssh.banner = """:
: Welcome to
:
:________                              ____________________  __
:___  __ \_________________ _______ _____  ___/_  ___/__  / / /
:__  / / /_  ___/  _ \  __ `/_  __ `__ \____ \_____ \__  /_/ /
:_  /_/ /_  /   /  __/ /_/ /_  / / / / /___/ /____/ /_  __  /
:/_____/ /_/    \___/\__,_/ /_/ /_/ /_//____/ /____/ /_/ /_/
:
:
: You have logged into a DreamSSH Server.
: {{HELP}}
:
: Enjoy!
:
"""

class Configurator(object):
    """
    """
    def __init__(self, main=None, ssh=None):
        self.main = main
        self.ssh = ssh
        self.updateConfig()

    def buildDefaults(self):
        config = SafeConfigParser()
        config.add_section("SSH")
        config.set("SSH", "servicename", self.ssh.servicename)
        config.set("SSH", "port", str(self.ssh.port))
        config.set("SSH", "pidfile", self.ssh.pidfile)
        config.set("SSH", "username", self.ssh.username)
        config.set("SSH", "keydir", self.ssh.keydir)
        config.set("SSH", "privkey", self.ssh.privkey)
        config.set("SSH", "pubkey", self.ssh.pubkey)
        config.set("SSH", "localdir", self.ssh.localdir)
        config.set("SSH", "banner", self.ssh.banner)
        return config


    def getConfigFile(self):
        if os.path.exists(self.main.config.localfile):
            return self.main.config.localfile
        if not os.path.exists(self.main.config.userdir):
            os.mkdir(os.path.expanduser(self.main.config.userdir))
        return self.main.config.userfile


    def writeDefaults(self):
        config = buildDefaults()
        with open(self.getConfigFile(), "wb") as configFile:
            config.write(configFile)

    def getConfig(self):
        configFile = self.getConfigFile()
        if not os.path.exists(configFile):
            self.writeDefaults()
            return
        config = SafeConfigParser()
        config.read(configFile)
        return config

    def updateConfig(self):
        """
        If the configfile doesn't exist, this method will (indirectly) create
        it and exit.

        If it does exist, it will load the config values from the file (which
        may be different from those defined be default in this module), and
        update the in-memory config values with what it reads from the file.
        """
        config = self.getConfig()
        if not config:
            return
        self.ssh.servicename = config.get("SSH", "servicename")
        self.ssh.port = int(config.get("SSH", "port"))
        self.ssh.pidfile = config.get("SSH", "pidfile")
        self.ssh.username = str(config.get("SSH", "username"))
        self.ssh.keydir = config.get("SSH", "keydir")
        self.ssh.privkey = config.get("SSH", "privkey")
        self.ssh.pubkey = config.get("SSH", "pubkey")
        self.ssh.localdir = config.get("SSH", "localdir")
        self.ssh.banner = str(config.get("SSH", "banner"))
        return config


Configurator(main, ssh)


del Config, Configurator
