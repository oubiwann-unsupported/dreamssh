from datetime import datetime
import os, subprocess

from twisted.conch.scripts import ckeygen
from twisted.internet import reactor
from twisted.python.filepath import FilePath
from twisted.web import client

from dreamssh.sdk import registry


config = registry.getConfig()


class Script(object):
    """
    """
    def __init__(self):
        self.run()

    def run(self):
        raise NotImplementedError()


class KeyGen(Script):
    """
    """
    def run(self):
        path = config.ssh.keydir
        key = os.path.join(path, "id_rsa")
        if not os.path.exists(path):
            print "Creating SSH key dir '%s' ..." % path
            os.makedirs(path)
        else:
            print "SSH key dir '%s' already exists." % path
        if not os.path.exists(key):
            print "Creating SSH key at '%s' ..." % key
            print "  (This could take a while)"
            options = {"filename": key, "bits": 4096, "pass": None}
            ckeygen.generateRSAkey(options)
        else:
            print "SSH key '%s' already exists." % key


class ConnectToShell(Script):
    """
    """
    def run(self):
        print "Connecting to %s ..." % config.ssh.servicename
        subprocess.call(["ssh",  "-p %s" % config.ssh.port,  config.ssh.ip])


class StopDaemon(Script):
    """
    """
    def run(self):
        print "Stopping %s ..." % config.ssh.servicename
        if not os.path.exists(config.ssh.pidfile):
            print "Could not find the server's PID file ..."
            print "Aborting."
        else:
            pid = open(config.ssh.pidfile).read()
            subprocess.call(["kill", pid])
            print "Stopped."


class GenerateConfig(Script):
    """
    """
    def backupConfig(self, src):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = FilePath("%s.%s" % (src.path, timestamp))
        # if something goes wrong with the setContent call, don't remove the
        # source!
        try:
            dest.setContent(src.open().read())
            src.remove()
        except Exception, e:
            raise e

    def run(self):
        # get config file path
        configurator = config.configuratorFactory()
        filePath = FilePath(configurator.getConfigFile())
        # check to see if it exists, and if so, back it up
        if filePath.exists():
            self.backupConfig(filePath)
        # write the new config
        configurator.writeDefaults()


class ImportKeys(Script):
    """
    """
    lp_template = "https://launchpad.net/~%s/+sshkeys"

    def __init__(self, username, lp_username=None):
        self.username = username
        if not lp_username:
            lp_username = username
        self.lp_url = self.lp_template % lp_username
        super(ImportKeys, self).__init__()

    def finish(self):
        reactor.stop()

    def createDirs(self):
        userDir = FilePath(config.ssh.userdirtemplate % self.username)
        if not userDir.exists():
            userDir.makedirs()

    def getAuthKeys(self):
        authKeys = FilePath(config.ssh.userauthkeys % self.username)
        data = None
        if authKeys.exists():
            data = authKeys.open()
        return (authKeys, data.read())

    def saveKeys(self, result):
        self.createDirs()
        filePath, data = self.getAuthKeys()
        if data:
            filePath.setContent("%s\n%s" % (data, result))
        else:
            filePath.setContent(result)
        self.finish()

    def logError(self, failure):
        print failure
        self.finish()

    def run(self):
        deferred = client.getPage(self.lp_url)
        deferred.addCallback(self.saveKeys)
        deferred.addErrback(self.logError)
        reactor.run()
