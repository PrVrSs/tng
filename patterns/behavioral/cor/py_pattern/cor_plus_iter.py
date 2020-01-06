import abc
import collections
from enum import Enum, auto


"""
Цепочка обязанности + итератор
"""


class TokenType(Enum):
    ZERO = auto()
    ONE = auto()
    TWO = auto()


class HandlerIterator(collections.Iterator):

    def __init__(self, handler, request):
        self._handler = handler
        self._request = request

    def __next__(self):
        if self._handler is not None:
            self._handler.handle_request(self._request)

        if self._handler.next_handler is None or self._handler is None:
            raise StopIteration()

        self._handler = self._handler.next_handler

        return self._handler


class HandlerIterable(collections.Iterable):
    def __init__(self, start_handler, request):
        self._request = request
        self._start_handler = start_handler

    def __iter__(self):
        return HandlerIterator(self._start_handler, self._request)


class Handler(metaclass=abc.ABCMeta):

    def __init__(self):
        self._next_handler = None

    @abc.abstractmethod
    def handle_request(self, request):
        pass

    def set_next_handler(self, handler):
        self._next_handler = handler

    @property
    def next_handler(self):
        return self._next_handler

    @next_handler.getter
    def next_handler(self):
        return self._next_handler


class ConcreteHandlerZero(Handler):

    def handle_request(self, request):
        print(f"It's handle for request: {TokenType.ZERO.name}")
        print(f"request: {request.name}")
        print('correct request') if request is TokenType.ZERO else print('incorrect request')


class ConcreteHandlerOne(Handler):

    def handle_request(self, request):
        print(f"It's handle for request: {TokenType.ONE.name}")
        print(f"request: {request.name}")
        print('correct request') if request is TokenType.ONE else print('incorrect request')


class ConcreteHandlerTwo(Handler):

    def handle_request(self, request):
        print(f"It's handle for request: {TokenType.TWO.name}")
        print(f"request: {request.name}")
        print('correct request') if request is TokenType.TWO else print('incorrect request')


def main():
    concrete_handler_zero: Handler = ConcreteHandlerZero()
    concrete_handler_one: Handler = ConcreteHandlerOne()
    concrete_handler_two: Handler = ConcreteHandlerTwo()

    concrete_handler_zero.set_next_handler(concrete_handler_one)
    concrete_handler_one.set_next_handler(concrete_handler_two)

    for _ in HandlerIterable(concrete_handler_zero, TokenType.ZERO):
        pass


if __name__ == "__main__":
    main()
