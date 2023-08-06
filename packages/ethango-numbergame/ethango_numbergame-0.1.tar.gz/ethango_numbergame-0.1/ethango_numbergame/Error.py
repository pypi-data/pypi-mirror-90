# define Python user-defined exceptions
class Error(Exception):
    """Base class for other exceptions"""
    pass


class ZeroOrLessError(Error):
    """Raised when the input value is Zero or a negative number"""
    pass