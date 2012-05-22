from zope.interface import Interface


class IConfig(Interface):
    """
    A marker interface for configuration objects.

    This interface is what is used to query the global registry for
    configuration instances.
    """


class ILogger(Interface):
    """
    A Marker interface for anything that does logging.
    """


class ITerminalWriter(Interface):
    """
    A marker interface for objects that can write data to a text-base user
    interface.
    """
