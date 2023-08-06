class PigmentError(Exception):
    """The base class for all Pigment exceptions"""

    pass


class WrongLengthError(PigmentError, ValueError):
    """The argument provided had an invalid length

    Note:
        Also a subclass of ``ValueError``

    Attributes:
        argument (str): The name of the argument
    """

    def __init__(self, argument: str = None):
        if argument:
            super().__init__("argument %s has an invalid length" % argument)
        else:
            super().__init__("argument has an invalid length")


class InvalidRGBValue(PigmentError, ValueError):
    """A value was invalid when converting or saving a color in RGB form

    Note:
        Also a subclass of ``ValueError``
    """

    def __init__(self):
        super().__init__("invalid RGB value")
