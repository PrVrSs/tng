import abc


class CaffeineBeverageWithHook(metaclass=abc.ABCMeta):

    def prepare_recipe(self):
        self.boil_water()
        self.brew()
        self.pour_in_cup()
        if self.customer_wants_condiments():
            self.add_condiments()

    @abc.abstractmethod
    def brew(self) -> None:
        pass

    @abc.abstractmethod
    def add_condiments(self) -> None:
        pass

    @staticmethod
    def boil_water() -> None:
        print('boil water')

    @staticmethod
    def pour_in_cup() -> None:
        print('Pour in cup')

    @staticmethod
    def customer_wants_condiments() -> bool:
        return True


class CoffeeWithHook(CaffeineBeverageWithHook):

    def brew(self) -> None:
        print('Brew coffee')

    def add_condiments(self) -> None:
        print('add sugar and milk')

    @staticmethod
    def customer_wants_condiments():
        return False


class TeaWithHook(CaffeineBeverageWithHook):

    def brew(self) -> None:
        print('Brew tea')

    def add_condiments(self) -> None:
        print('add lemon')

    @staticmethod
    def customer_wants_condiments():
        return True


def main():
    tea_hook: TeaWithHook = TeaWithHook()
    coffee_hook: CoffeeWithHook = CoffeeWithHook()
    print('**tee**')
    tea_hook.prepare_recipe()
    print('**coffee**')
    coffee_hook.prepare_recipe()


if __name__ == '__main__':
    main()
