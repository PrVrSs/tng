import abc


class Mediator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, sender, msg):
        pass

    @abc.abstractmethod
    def receive(self, mess):
        pass


class Server(metaclass=abc.ABCMeta):

    def __init__(self, mediator: Mediator):
        self._mediator = mediator

    @abc.abstractmethod
    def send(self, mess):
        pass

    @abc.abstractmethod
    def receive(self, mess):
        pass


class MediatorA(Mediator):

    def __init__(self):
        self._servers: list = []

    def add_server(self, server: Server):
        self._servers.append(server)

    def send(self, sender, msg):
        for server in self._servers:
            if sender is not server:
                pass

    def react_server_a(self):
        pass

    def react_server_b(self):
        pass


class ServerA(Server):

    def send(self, msg):
        self._mediator.send(self, msg)

    def receive(self, msg):
        pass


class ServerB(Server):

    def send(self, mess):
        pass

    def receive(self, mess):
        pass


def main():
    pass


if __name__ == "__main__":
    main()
