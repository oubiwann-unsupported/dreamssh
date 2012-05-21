import os
import subprocess

from twisted.conch.scripts import ckeygen

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
