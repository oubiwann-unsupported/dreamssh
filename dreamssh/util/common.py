from zope.component import getGlobalSiteManager, getUtility
from zope.interface.interfaces import ComponentLookupError

from dreamssh import interfaces


def getConfig():
    return getUtility(interfaces.IConfig)


def registerConfig(config):
    """
    For right now, only one configuration is allowed at a time.

    The way to use this is to register your config in the top-level __init__ of
    your project.

    This will be importing config, interfaces, and util.
    """
    try:
        config = getConfig()
    except ComponentLookupError:
        gsm = getGlobalSiteManager()
        gsm.registerUtility(config, interfaces.IConfig)
    return config
