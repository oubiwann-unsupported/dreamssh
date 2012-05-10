from twisted.application import service, internet
from twisted.python import usage

from dreamssh import config, const, exceptions, meta
from dreamssh.shell.service import getShellFactory


class Options(usage.Options):
    """
    """
    legalInterpreters = [const.PYTHON, const.ECHO]
    optParameters = [
        ["interpreter", "i", "python", 
         ("The interpreter to use; valid options incude: "
          ",".join(legalInterpreters))]
         ]


def makeService(options):
    # check options
    interpreterType = options.get("interpreter")
    if interpreterType and interpreterType not in Options.legalInterpreters:
        raise exceptions.UnsupportedInterpreterType()

    # primary setup
    application = service.Application(meta.description)
    services = service.IServiceCollection(application)

    # setup ssh access to a Python shell
    sshFactory = getShellFactory(
        interpreterType, app=application, services=services)
    sshserver = internet.TCPServer(config.ssh.port, sshFactory)
    sshserver.setName(config.ssh.servicename)
    sshserver.setServiceParent(services)

    return services
