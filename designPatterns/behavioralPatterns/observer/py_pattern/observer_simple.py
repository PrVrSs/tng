import abc


class AbstractDisplay(metaclass=abc.ABCMeta):
    pass


class AbstractObserver(metaclass=abc.ABCMeta):
    pass


class AbstractSubject(metaclass=abc.ABCMeta):
    pass


class CurrentConditionsDisplay(AbstractObserver, AbstractDisplay):

    def __init__(self):
        super().__init__()
        self._observers: list = []
        self._temperature: float = 0
        self._humidity: float = 0
        self._pressure: float = 0

    def update(self, temperature: float):
        self._temperature = temperature
        self.display()

    def display(self):
        print(self._temperature)


class WeatherData(AbstractSubject):

    def __init__(self):
        super().__init__()
        self._observers: list = []
        self._temperature: float = 0
        self._humidity: float = 0
        self._pressure: float = 0

    def register_observer(self, observer: AbstractObserver=None):
        if observer is not None:
            self._observers.append(observer)

    def remove_observer(self, observer: AbstractObserver):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify_observer(self):
        for observer in self._observers:
            observer.update(self._temperature)

    def measurements_changed(self):
        self.notify_observer()

    def set_measurements(self, temperature: float):
        self._temperature: float = temperature
        self.measurements_changed()


def main():
    weather_data_1: WeatherData = WeatherData()
    current_conditions_display_1: CurrentConditionsDisplay = CurrentConditionsDisplay()
    current_conditions_display_2: CurrentConditionsDisplay = CurrentConditionsDisplay()
    weather_data_1.register_observer(current_conditions_display_1)
    weather_data_1.register_observer(current_conditions_display_2)
    weather_data_1.set_measurements(100)


if __name__ == '__main__':
    main()
