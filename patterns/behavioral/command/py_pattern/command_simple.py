import abc


"""
Device
"""


class Light(object):
    def __init__(self):
        self._name = 'Light'

    def on(self):
        print(f"{self._name} turn on")

    def off(self):
        print(f"{self._name} turn off")


class CeilingFan(object):

    def __init__(self):
        self._name = 'Ceiling'
        self._speed: int = 0

    def low(self):
        print(f"{self._name} low")
        self._speed = 1

    def medium(self):
        print(f"{self._name} medium")
        self._speed = 2

    def high(self):
        print(f"{self._name} high")
        self._speed = 3

    def off(self):
        print(f"{self._name} off")
        self._speed = 0

    def get_speed(self):
        return self._speed


"""
Command
"""


class Command(abc.ABC):

    @abc.abstractmethod
    def execute(self):
        """
        :return:
        """

    @abc.abstractmethod
    def undo(self):
        """
        :return:
        """


class LightOnCommand(Command):

    def __init__(self, light: Light=None):
        self._light: Light = light

    def execute(self) -> None:
        self._light.on()

    def undo(self) -> None:
        self._light.off()


class LightOffCommand(Command):

    def __init__(self, light: Light = None):
        self._light: Light = light

    def execute(self) -> None:
        self._light.off()

    def undo(self) -> None:
        self._light.on()


class CeilingCommand(Command):

    def __init__(self, ceiling_fan: CeilingFan=None):
        self._ceiling_fan = ceiling_fan
        self._prev_speed: None = 0

    @abc.abstractmethod
    def execute(self):
        """
        :return:
        """

    def undo(self):
        if self._prev_speed == 3:
            self._ceiling_fan.high()
        elif self._prev_speed == 2:
            self._ceiling_fan.medium()
        elif self._prev_speed == 1:
            self._ceiling_fan.low()
        elif self._prev_speed == 0:
            self._ceiling_fan.off()


class CeilingFanHighCommand(CeilingCommand):

    def execute(self):
        self._prev_speed = self._ceiling_fan.get_speed()
        self._ceiling_fan.high()


class CeilingFanMediumCommand(CeilingCommand):

    def execute(self):
        self._prev_speed = self._ceiling_fan.get_speed()
        self._ceiling_fan.medium()


class CeilingFanOffCommand(CeilingCommand):

    def execute(self):
        self._prev_speed = self._ceiling_fan.get_speed()
        self._ceiling_fan.off()


"""
RemoteControl
"""


class RemoteControl(object):

    def __init__(self):
        self._on_commands: list = [0 for _ in range(7)]
        self._off_commands: list = [0 for _ in range(7)]
        self._undo_command: Command = None

    def set_command(self, slot: int=0, on_command: Command = None, off_command: Command = None):
        self._on_commands[slot] = on_command
        self._off_commands[slot] = off_command

    def on_button_was_pushed(self, slot: int=0):
        self._on_commands[slot].execute()
        self._undo_command = self._on_commands[slot]

    def off_button_was_pushed(self, slot: int=0):
        self._off_commands[slot].execute()
        self._undo_command = self._off_commands[slot]

    def undo_button_was_pushed(self):
        self._undo_command.undo()


def main():
    remote_control: RemoteControl = RemoteControl()

    light: Light = Light()

    light_on_command: Command = LightOnCommand(light=light)
    light_off_command: Command = LightOffCommand(light=light)

    remote_control.set_command(slot=0, on_command=light_on_command, off_command=light_off_command)

    remote_control.on_button_was_pushed(0)
    remote_control.undo_button_was_pushed()

    remote_control.on_button_was_pushed(0)
    remote_control.off_button_was_pushed(0)

    ceiling_fan: CeilingFan = CeilingFan()

    ceiling_fan_medium_command: Command = CeilingFanMediumCommand(ceiling_fan=ceiling_fan)
    ceiling_fan_high_command: Command = CeilingFanHighCommand(ceiling_fan=ceiling_fan)
    ceiling_fan_off_command: Command = CeilingFanOffCommand(ceiling_fan=ceiling_fan)

    remote_control.set_command(slot=1, on_command=ceiling_fan_medium_command, off_command=ceiling_fan_off_command)
    remote_control.set_command(slot=2, on_command=ceiling_fan_high_command, off_command=ceiling_fan_off_command)

    remote_control.on_button_was_pushed(1)
    remote_control.on_button_was_pushed(2)
    remote_control.undo_button_was_pushed()


if __name__ == '__main__':
    main()
