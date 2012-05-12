import os
import subprocess

from twisted.conch.scripts import ckeygen

from dreamssh import config


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
        print "Connecting to DreamSSH Server ..."
        subprocess.call(["ssh",  "-p %s" % config.ssh.port,  "127.0.0.1"])


class StopDaemon(Script):
    """
    """
    def run(self):
        print "Stopping DreamSSH Server ..."
        if not os.path.exists(config.ssh.pidfile):
            print "Could not find the server's PID file ..."
            print "Aborting."
        else:
            pid = open(config.ssh.pidfile).read()
            subprocess.call(["kill", pid])
            print "Stopped."
