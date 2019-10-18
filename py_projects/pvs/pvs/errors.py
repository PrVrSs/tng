"""Custom Exception"""


class ItemAlreadyStored(Exception):
    pass


class ItemNotStored(Exception):
    pass


class CutterException(Exception):
    """General Cutter exception occurred."""


class CMDException(Exception):
    """General Cmd exception occurred."""


class ArgumentValidationError(ValueError):
    """
    Raised when the type of an argument to a function is not what it should be.
    """

    def __init__(self, arg_num: int, func_name: str, accepted_arg_type: str):
        super().__init__()

        self.error: str = f'The {arg_num} argument of {func_name}() is not a {accepted_arg_type}'

    def __str__(self) -> str:
        return self.error


class InvalidArgumentNumberError(ValueError):
    """
    Raised when the number of arguments supplied to a function is incorrect.
    Note that this check is only performed from the number of arguments
    specified in the validate_accept() decorator. If the validate_accept()
    call is incorrect, it is possible to have a valid function where this
    will report a false validation.
    """

    def __init__(self, func_name):
        super().__init__()

        self.error: str = f'Invalid number of arguments for {func_name}()'

    def __str__(self) -> str:
        return self.error
