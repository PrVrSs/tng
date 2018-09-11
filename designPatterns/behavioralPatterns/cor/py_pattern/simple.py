import abc
from enum import Enum, auto


"""
Цепочка обязанности
"""


class TokenType(Enum):
    ZERO = auto()
    ONE = auto()
    TWO = auto()


class Handler(metaclass=abc.ABCMeta):

    def __init__(self):
        self._next_handler = None

    @abc.abstractmethod
    def handle_request(self, request):
        pass

    def set_next_handler(self, handler):
        self._next_handler = handler


class ConcreteHandlerZero(Handler):

    def handle_request(self, request):
        print(f"It's handle for request: {TokenType.ZERO.name}")
        print(f"request: {request.name}")
        if request is TokenType.ZERO:
            print('correct request')
        else:
            print('incorrect request')
            if self._next_handler is not None:
                print('load next handle in chain...')
                self._next_handler.handle_request(request)


class ConcreteHandlerOne(Handler):

    def handle_request(self, request):
        print(f"It's handle for request: {TokenType.ONE.name}")
        if request is TokenType.ONE:
            print('correct request')
        else:
            print('incorrect request')
            if self._next_handler is not None:
                print('load next handle in chain...')
                self._next_handler.handle_request(request)


class ConcreteHandlerTwo(Handler):

    def handle_request(self, request):
        print(f"It's handle for request: {TokenType.TWO.name}")
        if request is TokenType.TWO:
            print('correct request')
        else:
            print('incorrect request')
            if self._next_handler is not None:
                print('load next handle in chain...')
                self._next_handler.handle_request(request)


def main():
    concrete_handler_zero: Handler = ConcreteHandlerZero()
    concrete_handler_one: Handler = ConcreteHandlerOne()
    concrete_handler_two: Handler = ConcreteHandlerTwo()

    concrete_handler_zero.set_next_handler(concrete_handler_one)
    concrete_handler_one.set_next_handler(concrete_handler_two)

    concrete_handler_zero.handle_request(TokenType.ZERO)
    concrete_handler_zero.handle_request(TokenType.ONE)
    concrete_handler_zero.handle_request(TokenType.TWO)


if __name__ == "__main__":
    main()
