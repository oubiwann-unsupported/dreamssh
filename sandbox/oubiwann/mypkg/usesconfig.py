from mypkg.interfaces import IMyConfig
from mypkg.config import config
from mypkg.util import registry

def do_an_app_thing():
    # get config
    return IMyApp(app).get_config()


def do_a_config_thing():
    # get config
    #import pdb;pdb.set_trace()
    return IMyConfig(config).get_attr()


def do_a_config_thing_2():
    return registry.get("config")

def do_a_config_thing_2():
    return registry.get("config")
"""
---------------------------------
Thought 1:

duck quacks like duck
platypus quacks like duck
hunter does not quack like duck
duckcall adapts hunter to quack like duck

---------------------------------
Thought 2:

the players:
 * duck - quacks
 * platypus
 * hunter

the players:
 * config - has app data

---------------------------------
Thought 3:

base app, running base app, gets base config
base app, running other app, gets other config

---------------------------------
Thought 4:

adapt to running app
base app
running app config

adapt to running app
other app
running app config

---------------------------------
Thought 5:

adapt to running app
base app
IRunningApp

adapt to running app
other app
IRunningApp

adapter, base app, and running app all have a "get config" method

---------------------------------
Thought 6:

adapt given config to running config
base config
IRunningConfig

...?

"""
