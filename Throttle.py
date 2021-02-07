import math
import threading
import time

import Command
import Config
import Input
import Event

max_speed_kmh = 0

THROTTLE_UP = 0
THROTTLE_DOWN = 1
THROTTLE_NONE = 2


def init():
    global max_speed_kmh
    if 'max_speed_kmh' in Config.config:
        max_speed_kmh = Config.config['max_speed_kmh']

    thread = threading.Thread(target=manage_input_event)
    thread.start()


def manage_input_event():
    print("Throttle init")
    global max_speed_kmh

    while True:
        Event.wait()

        if max_speed_kmh != 0:
            norm_speed_ms = Input.get_norm_speed()
            norm_speed_kmh = norm_speed_ms / 1000.0 * 3600

            if norm_speed_kmh < max_speed_kmh - max_speed_kmh * 0.05:
                Command.TRUCK_BRAKE(0)
                Command.TRUCK_ACCELERATE(100)
            else:
                if norm_speed_kmh > max_speed_kmh:
                    Command.TRUCK_BRAKE(100)
                    Command.TRUCK_ACCELERATE(0)
                else:
                    Command.TRUCK_BRAKE(0)
                    Command.TRUCK_ACCELERATE(0)
        else:
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(100)


def set_max_speed(speed_kmh):
    global max_speed_kmh
    max_speed_kmh = speed_kmh
