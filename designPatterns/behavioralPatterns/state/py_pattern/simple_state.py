import abc
import random


class State(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def insert_quarter(self):
        pass

    @abc.abstractmethod
    def eject_quarter(self):
        pass

    @abc.abstractmethod
    def turn_crank(self):
        pass

    @abc.abstractmethod
    def dispense(self):
        pass


class GumballMachine(object):

    def __init__(self, number_gumballs: int=0):
        self._sold_out_state: State = SoldOutState(self)
        self._no_quarter_state: State = NoQuarterState(self)
        self._has_quarter_state: State = HasQuarterState(self)
        self._sold_state: State = SoldState(self)
        self._winner_state: State = WinnerState(self)
        self._number_gumballs: int = number_gumballs
        self._state = self._no_quarter_state if self._number_gumballs > 0 else self._sold_out_state

    def insert_quarter(self) -> None:
        self._state.insert_quarter()

    def eject_quarter(self) -> None:
        self._state.eject_quarter()

    def turn_crank(self) -> None:
        self._state.turn_crank()
        self._state.dispense()

    def set_state(self, state: State=None) -> None:
        if state is not None:
            self._state = state

    def release_ball(self) -> None:
        print('A gumball comes rolling out the slot...')
        if self._number_gumballs is not 0:
            self._number_gumballs -= 1

    def get_count(self) -> int:
        return self._number_gumballs

    def get_has_quarter_state(self) -> State:
        return self._has_quarter_state

    def get_sold_out_state(self) -> State:
        return self._sold_out_state

    def get_no_quarter_state(self) -> State:
        return self._no_quarter_state

    def get_sold_state(self) -> State:
        return self._sold_state

    def get_winner_state(self) -> State:
        return self._winner_state


class WinnerState(State):

    def __init__(self, gumball_machine: GumballMachine):
        self._gumball_machine: GumballMachine = gumball_machine

    def insert_quarter(self):
        print('WinnerState')

    def eject_quarter(self):
        print('WinnerState')

    def turn_crank(self):
        print('WinnerState')

    def dispense(self):
        print('You\'re a winner! you get who gubball for your quarter')
        self._gumball_machine.release_ball()
        if self._gumball_machine.get_count() == 0:
            self._gumball_machine.set_state(self._gumball_machine.get_sold_state())
        else:
            self._gumball_machine.release_ball()
            if self._gumball_machine.get_count() > 0:
                self._gumball_machine.set_state(self._gumball_machine.get_no_quarter_state())
            else:
                print('Ooops, out of gumballs')
                self._gumball_machine.set_state(self._gumball_machine.get_sold_out_state())


class SoldState(State):

    def __init__(self, gumball_machine: GumballMachine):
        self._gumball_machine: GumballMachine = gumball_machine

    def insert_quarter(self):
        pass

    def eject_quarter(self):
        pass

    def turn_crank(self):
        pass

    def dispense(self):
        self._gumball_machine.release_ball()
        if self._gumball_machine.get_count() > 0:
            self._gumball_machine.set_state(self._gumball_machine.get_no_quarter_state())
        else:
            print('Ooops, out of gumball')
            self._gumball_machine.set_state(self._gumball_machine.get_sold_out_state())


class SoldOutState(State):

    def __init__(self, gumball_machine: GumballMachine):
        self._gumball_machine: GumballMachine = gumball_machine

    def insert_quarter(self):
        print('NO BALLS')

    def eject_quarter(self):
        print('NO BALLS')

    def turn_crank(self):
        print('NO BALLS')

    def dispense(self):
        print('NO BALLS')


class NoQuarterState(State):

    def __init__(self, gumball_machine: GumballMachine):
        self._gumball_machine: GumballMachine = gumball_machine

    def insert_quarter(self):
        print('You inserted a quarter')
        self._gumball_machine.set_state(self._gumball_machine.get_has_quarter_state())

    def eject_quarter(self):
        print('You haven\'t inserted a quarter')

    def turn_crank(self):
        print('You turned, but there\'s no quarter')

    def dispense(self):
        print('You need to pay first')


class HasQuarterState(State):

    def __init__(self, gumball_machine: GumballMachine):
        self._gumball_machine: GumballMachine = gumball_machine

    def insert_quarter(self):
        print('You can\'t insert another quarter')

    def eject_quarter(self):
        print('Quarter returned')
        self._gumball_machine.set_state(self._gumball_machine.get_no_quarter_state())

    def turn_crank(self):
        winner: int = random.randint(0, 9)
        if winner == 0 and self._gumball_machine.get_count() > 1:
            self._gumball_machine.set_state(self._gumball_machine.get_winner_state())
        else:
            self._gumball_machine.set_state(self._gumball_machine.get_sold_state())

    def dispense(self):
        print('No gumball dispensed')


def main():
    gumball_machine: GumballMachine = GumballMachine(5)

    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()

    gumball_machine.insert_quarter()
    gumball_machine.eject_quarter()
    gumball_machine.turn_crank()

    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()

    gumball_machine.insert_quarter()
    gumball_machine.turn_crank()


if __name__ == '__main__':
    main()
