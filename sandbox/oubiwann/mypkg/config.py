"""
when mypkg.config is imported in mypkg.*, I want to return configuration for
mypkg

however, when mypkg.config is imported in otherpkg.*, I want to return the
configuration for otherpkg

as such, if a module that calls config registers an adaptor, then when the
config module is imported, the registration will have already happened, and
the registry lookup can get the appropriate adaptor

app.py
 * import interfaces.IMyApp
 * import MyAp
 * import AdaptConfigToApp
 * components.registerAdapter(AdaptConfigToApp, , IMyApp)

config.py
 * 

"""
from zope.interface import implements

from mypkg.interfaces import IMyConfig


class MyConfig(object):
    implements(IMyConfig)
    def get_attr(self):
        return "a my attr datum"


config = MyConfig()
config.name = "mypkg config"
config.a = 1
config.b = 2
config.c = MyConfig()
config.c.d = 3
config.c.e = 4
config.c.f = 5
config.g = 6
config.h = 7
