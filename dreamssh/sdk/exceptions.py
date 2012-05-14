class Error(Exception):
    """
    A base class for exceptions.
    """
    def __init__(self, msg=None):
        if msg == None:
            msg = self.__doc__.strip()
        super(Error, self).__init__(msg)


class MissingSSHServerKeysError(Error):
    """
    SSH server keys not found. Generate them with 'twistd dreamssh keygen'
    """


class IllegalAPICommand(Error):
    """
    """


class UnsupportedInterpreterType(Error):
    """
    The interpreter type specified is not supported.
    """


class UnsupportedSubsystemError(Error):
    """
    """
