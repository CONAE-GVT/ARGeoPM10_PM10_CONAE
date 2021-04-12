class EmpatiaBaseException(Exception):
    pass


class DirDoesntExists(EmpatiaBaseException):
    pass


class FileExists(EmpatiaBaseException):
    """
        The file provided already exists.
    """


class FileDoesNotExist(EmpatiaBaseException):
    """
        The file provided does not exist.
    """
