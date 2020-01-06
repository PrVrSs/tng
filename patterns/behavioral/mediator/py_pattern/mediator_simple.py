import abc


class Mediator(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def send(self, sender, msg: str=''):
        pass


class Server(metaclass=abc.ABCMeta):

    def __init__(self, mediator: Mediator):
        self._mediator: Mediator = mediator
        self._name = ''

    def receive(self, msg: str='', server=None) -> None:
        print(f'{self._name} receive msg: {msg}. From {server}')

    @abc.abstractmethod
    def send(self, msg) -> None:
        pass

    def __repr__(self):
        return f'{self._name}'


class ServersMediator(Mediator):

    def __init__(self):
        self._servers: list = []

    def add_server(self, server: Server) -> None:
        self._servers.append(server)

    def send(self, sender: Server, msg: str='') -> None:
        for server in self._servers:
            if sender is not server:
                server.receive(msg, sender)


class ServerA(Server):

    def __init__(self, mediator):
        super(ServerA, self).__init__(mediator)
        self._name = 'ServerA'

    def send(self, msg: str='') -> None:
        self._mediator.send(self, msg)


class ServerB(Server):

    def __init__(self, mediator):
        super(ServerB, self).__init__(mediator)
        self._name = 'ServerB'

    def send(self, msg: str = '') -> None:
        self._mediator.send(self, msg)


def main():
    mediator: ServersMediator = ServersMediator()
    server_a: Server = ServerA(mediator)
    server_b: Server = ServerB(mediator)
    mediator.add_server(server_a)
    mediator.add_server(server_b)
    server_a.send('I\'m server A')
    server_b.send('I\'m server B')


if __name__ == '__main__':
    main()
