from zope.component import getUtility

from dreamssh import interfaces


def getConfig():
    return getUtility(interfaces.IConfig)
