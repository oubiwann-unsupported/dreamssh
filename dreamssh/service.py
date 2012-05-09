from twisted.application import service, internet
from twisted.python import usage

from dreamssh import config, meta
from dreamssh.shell.service import getShellFactory


class Options(usage.Options):
    """
    """
    # XXX add options for determining which interpreter to run


def makeService(options):
    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)

    # setup ssh access to a Python shell
    sshFactory = getShellFactory(app=application, services=services)
    sshserver = internet.TCPServer(config.ssh.port, sshFactory)
    sshserver.setName(config.ssh.servicename)
    sshserver.setServiceParent(services)

    return services
