"""
I attempted to use components to do configuration, but as you can see in
mypkg.usesconfig, the config instance that I would need to adapt is imported,
thus already preventing the possible use of this code by another project with a
different config.

It seems the best way to get what I want will be a global registry.
"""
from zope.component import getGlobalSiteManager, getUtility
from zope.interface import Interface, implements

from twisted.python import components

from mypkg.interfaces import IMyApp, IMyConfig
from mypkg.util import registry


def check_config_base_3():
    from mypkg import config, interfaces, usesconfig
    gsm = getGlobalSiteManager()
    gsm.registerUtility(config, interfaces.IConfig)
    usesconfig.do_a_config_thing_3()


def check_config_inherited_3():
    from mypkg import interfaces, usesconfig
    from otherpkg import config

    gsm = getGlobalSiteManager()
    gsm.registerUtility(config, interfaces.IConfig)
    usesconfig.do_a_config_thing_3()


def check_config_base_2():
    from mypkg import config, interfaces, usesconfig

    registry["config"] = config
    print usesconfig.do_a_config_thing_2()


def check_config_inherited_2():
    from otherpkg import config
    from mypkg import interfaces, usesconfig

    registry["config"] = config
    print usesconfig.do_a_config_thing_2()


class AdaptRunningConfigToMyConfig(object):
    implements(IMyConfig)
    def __init__(self, config):
        self.config = config
    def get_attr(self):
        return self.config.name


class AdaptRunningAppToMyApp(object):
    implements(IMyApp)
    def __init__(self, app):
        self.app = app
    def get_config(self):
        return self.app.config


def check_config_base():
    from mypkg import config, interfaces, usesconfig

    components.registerAdapter(
        AdaptRunningConfigToMyConfig, config.MyConfig, IMyConfig)

    print usesconfig.do_a_config_thing()


def check_config_inherited():
    from mypkg import usesconfig
    from otherpkg import config

    class OtherConfig(object):
        def get_attr(self):
            return "an other attr datum"

    components.registerAdapter(
        AdaptRunningConfigToMyConfig, config.OtherConfig, IMyConfig)

    print usesconfig.do_a_config_thing()


def check_app_base():
    from mypkg import config

    class IMyApp(Interface):
        def get_config():
            pass

    class MyApp(object):
        def get_config(self):
            return "config.name = 'my app'"

    components.registerAdapter(
        AdaptRunningAppToMyApp, MyApp, IMyApp)


def check_app_inherited():
    from otherpkg import config

    class OtherApp(object):
        def get_config(self):
            return "config.name = 'other app'"

    components.registerAdapter(
        AdaptRunningAppToMyApp, OtherApp, IMyApp)

if __name__ == "__main__":
    check_config_base_3()
    check_config_inherited_3()
