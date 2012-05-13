from zope.interface import implements

from mypkg.interfaces import IConfig


class OtherConfig(object):
    implements(IConfig)
    def get_attr(self):
        return "an other attr datum"


config = OtherConfig()
config.name = "otherpkg config"
config.a = 7
config.b = 6
config.c = OtherConfig()
config.c.d = 5
config.c.e = 4
config.c.f = 3
config.g = 2
config.h = 1
