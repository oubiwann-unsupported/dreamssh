from twisted.web import vhost
from twisted.web import server
from twisted.web import static
from twisted.application import service, internet
from twisted.internet.protocol import ServerFactory
from twisted.internet.ssl import ClientContextFactory

from inversum import auth, config, meta
from inversum.shell.base import getShellFactory


# primary setup
application = service.Application(meta.description)
services = service.IServiceCollection(application)

# setup ssh access to a Python shell
sshFactory = getShellFactory(app=application, services=services)
sshserver = internet.TCPServer(config.ssh.port, sshFactory)
sshserver.setName(config.ssh.servicename)
sshserver.setServiceParent(services)
