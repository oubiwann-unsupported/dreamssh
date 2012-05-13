from zope.interface import Interface


class IMyApp(Interface):
    """
    """
    def get_config(self):
        """
        Get the config object.
        """

class IMyConfig(Interface):
    """
    """
    def get_attr(self):
        """
        """
