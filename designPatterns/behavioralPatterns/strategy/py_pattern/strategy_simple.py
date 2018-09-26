import abc


class FlyBehavior(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def fly(self) -> None:
        pass


class QuackBehavior(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def quack(self) -> None:
        pass


class Duck(metaclass=abc.ABCMeta):

    def __init__(self, fly_behavior: FlyBehavior=None, quack_behavior: QuackBehavior=None):
        self._fly_behavior: FlyBehavior = fly_behavior
        self._quack_behavior: QuackBehavior = quack_behavior

    @abc.abstractmethod
    def display(self):
        pass

    def perform_fly(self) -> None:
        self._fly_behavior.fly()

    def perform_quack(self) -> None:
        self._quack_behavior.quack()

    @staticmethod
    def swim() -> None:
        print('All ducks float, even  decoys!')

    def set_fly_behavior(self, fly_behavior: FlyBehavior=None):
        self._fly_behavior = fly_behavior

    def set_quack_behavior(self, quack_behavior: QuackBehavior = None):
        self._quack_behavior = quack_behavior


class Quack(QuackBehavior):

    def quack(self):
        print('Quack')


class MuteQuack(QuackBehavior):

    def quack(self):
        print('<< Silence >>')


class FlyWithWings(FlyBehavior):

    def fly(self):
        print('I\'m flying')


class FlyNoWay(FlyBehavior):

    def fly(self):
        print('I can\'t fly')


class ModelDuck(Duck):
    def __init__(self):
        super().__init__()
        self._fly_behavior: FlyBehavior = FlyNoWay()
        self._quack_behavior: QuackBehavior = MuteQuack()

    def display(self):
        print('Model Duck')


class MallardDuck(Duck):
    def __init__(self):
        super().__init__()
        self._fly_behavior: FlyBehavior = FlyWithWings()
        self._quack_behavior: QuackBehavior = Quack()

    def display(self):
        print('Mallard Duck')


def main():
    mallard: Duck = MallardDuck()
    mallard.display()
    mallard.perform_fly()
    mallard.perform_quack()

    model: Duck = ModelDuck()
    model.display()
    model.perform_fly()
    model.perform_quack()
    model.set_quack_behavior(Quack())
    model.perform_quack()


if __name__ == '__main__':
    main()
