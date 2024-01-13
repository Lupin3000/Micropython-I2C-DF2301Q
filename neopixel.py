from lib.DFRobot_DF2301Q_I2C import DFRobot_DF2301Q_I2C
from machine import Pin
from micropython import const
from utime import sleep
from neopixel import NeoPixel


SDA_PIN = const(21)
SCL_PIN = const(22)

NEOPIXEL_PIN = const(16)
NEOPIXEL_NUMBER = const(5)

SLEEP_SECONDS = const(1)
TURN_ON_COMMAND = const(103)
TURN_OFF_COMMAND = const(104)
COLOR_COMMANDS = {
    116: ("red", (250, 0, 0)),
    117: ("orange", (250, 165, 0)),
    118: ("yellow", (250, 255, 204)),
    119: ("green", (0, 250, 0)),
    120: ("cyan", (0, 255, 255)),
    121: ("blue", (0, 0, 250)),
    122: ("purple", (128, 0, 128)),
    123: ("white", (250, 250, 250))
}


def setup(sensor) -> None:
    """
    Set up the DFRobot DF2301Q sensor
    :param sensor: instance of DFRobot_DF2301Q_I2C
    :return: None
    """
    sensor.set_volume(5)
    sensor.set_mute_mode(0)
    sensor.set_wake_time(20)


def get_cmd_id(sensor) -> int:
    """
    Get the command id back from the DF2301Q sensor
    :param sensor: instance of DFRobot_DF2301Q_I2C
    :return: int
    """
    command_id = sensor.get_cmdid()

    if command_id != 0:
        return int(command_id)


def set_color(neopixel, rgb) -> None:
    """
    Set the color of neopixel
    :param neopixel: instance of neopixel
    :param rgb: rgb color as tuple
    :return: None
    """
    neopixel.fill(rgb)
    neopixel.write()


if __name__ == "__main__":
    nps = NeoPixel(Pin(NEOPIXEL_PIN), NEOPIXEL_NUMBER)
    voice_sensor = DFRobot_DF2301Q_I2C(sda=SDA_PIN, scl=SCL_PIN)
    setup(sensor=voice_sensor)

    last_color = None
    light_on = False

    print('Speak your commands:')

    while True:
        cmd_id = get_cmd_id(sensor=voice_sensor)

        if isinstance(cmd_id, int):
            print(f'COMMAND ID: {cmd_id}')

            command_info = COLOR_COMMANDS.get(cmd_id)

            # turn on the light
            if cmd_id == TURN_ON_COMMAND:
                light_on = True

                if not last_color:
                    set_color(neopixel=nps, rgb=(100, 100, 100))
                else:
                    set_color(neopixel=nps, rgb=last_color)

            # turn off the light
            if cmd_id == TURN_OFF_COMMAND:
                light_on = False
                set_color(neopixel=nps, rgb=(0, 0, 0))

            # set to [color name]
            if command_info is not None and light_on:
                name, color = command_info
                last_color = color
                set_color(neopixel=nps, rgb=color)

        sleep(SLEEP_SECONDS)
