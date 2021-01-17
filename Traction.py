import math
import threading
import time

import Command
import Config
import Input
import Event

go_forward = True
max_speed_kmh = 0
max_speed_increase = 0
traction_force = 100


def init():
    global max_speed_kmh
    if 'max_speed_kmh' in Config.config:
        max_speed_kmh = Config.config['max_speed_kmh']

    thread = threading.Thread(target=manage_input_event)
    thread.start()


def manage_input_event():
    print("Traction init")
    global max_speed_kmh
    global traction_force

    num_previous_speed = 4
    previous_speed_array = []

    for i in range(0, num_previous_speed):
        previous_speed_array.append(1000000.0)

    while True:
        Event.wait()

        if max_speed_kmh != 0:
            norm_speed_ms = Input.get_norm_speed()
            norm_speed_kmh = norm_speed_ms / 1000.0 * 3600

            if norm_speed_kmh < max_speed_kmh:
                traction_on(traction_force)
            else:
                if norm_speed_kmh > max_speed_kmh + max_speed_kmh * 0.1:
                    traction_off(traction_force)
                else:
                    traction_off(0)

                traction_force -= 5

            previous_speed_array.pop(0)
            previous_speed_array.append(norm_speed_kmh)

            prev_speed = 1000000.0
            decelerate = True
            for s in previous_speed_array:
                if s <= prev_speed:
                    prev_speed = s
                    continue
                else:
                    decelerate = False

            if decelerate is True:
                traction_force += 5
                if traction_force > 100:
                    traction_force = 100

        else:
            traction_on(100)


def forward():
    global go_forward
    go_forward = True


def backward():
    global go_forward
    go_forward = False


def traction_on(value):
    global go_forward
    if go_forward is True:
        Command.brake(0)
        Command.accelerate(value)
    else:
        Command.accelerate(0)
        Command.brake(value)


def traction_off(value):
    global go_forward
    if go_forward is False:
        Command.brake(0)
        Command.accelerate(value)
    else:
        Command.accelerate(0)
        Command.brake(value)


def set_max_speed(speed_kmh):
    global max_speed_kmh
    global traction_force
    max_speed_kmh = speed_kmh
    traction_force = 100
