from zope.interface import implements

from twisted.cred import checkers, portal
from twisted.web import guard, http, resource, static

from inversum import config


class BasicAuthRealm(object):
    """
    """
    implements(portal.IRealm)

    def __init__(self, resource):
        self.resource = resource

    def requestAvatar(self, avatarId, mind, *interfaces):
        if resource.IResource in interfaces:
            return (
                resource.IResource, 
                self.resource,
                lambda: None)
        raise NotImplementedError()


def guardResourceWithBasicAuth(resource, realm, db):
    checker = checkers.InMemoryUsernamePasswordDatabaseDontUse(**db)
    logPortal = portal.Portal(BasicAuthRealm(resource), [checker])
    credentialFactory = guard.BasicCredentialFactory("%s:%s" % (
        config.log.http.vhost, config.log.http.port))
    return guard.HTTPAuthSessionWrapper(logPortal, [credentialFactory])
