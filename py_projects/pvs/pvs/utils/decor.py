import functools
from typing import Tuple, Type

from ..errors import InvalidArgumentNumberError, ArgumentValidationError


STRING_TYPES: Tuple[Type[bytes], Type[str]] = (type(b''), type(u''))


def accepts(*accepted_arg_types):

    def accept_decorator(validate_function):

        @functools.wraps(validate_function)
        def decorator_wrapper(*args, **kwargs):
            if len(accepted_arg_types) is not len(accepted_arg_types):
                raise InvalidArgumentNumberError(validate_function.__name__)

            for arg_num, (actual_arg, accepted_arg_type) in enumerate(zip(args[1:], accepted_arg_types)):
                if not isinstance(actual_arg, accepted_arg_type):
                    ord_num = arg_num + 1
                    raise ArgumentValidationError(ord_num,
                                                  validate_function.__name__,
                                                  accepted_arg_type)

            return validate_function(*args, **kwargs)

        return decorator_wrapper

    return accept_decorator
