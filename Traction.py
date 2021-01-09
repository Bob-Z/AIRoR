import math
import threading
import time

import Command
import Config
import Input
import Event

is_forward = True
max_speed_kmh = 0
max_speed_increase = 0


def init():
    thread = threading.Thread(target=manage_input_event)
    thread.start()

    global max_speed_kmh
    if 'max_speed_kmh' in Config.config:
        max_speed_kmh = Config.config['max_speed_kmh']


def manage_input_event():
    global max_speed_increase
    global max_speed_kmh

    while True:
        Event.wait()
        traction_off()

        if max_speed_kmh != 0:
            speed = Input.get_speed()
            norm_speed_ms = math.sqrt(speed[0] * speed[0] + speed[1] * speed[1] + speed[2] * speed[2])
            norm_speed_kmh = norm_speed_ms / 1000.0 * 3600

            if norm_speed_kmh < max_speed_kmh:
                if norm_speed_kmh < max_speed_kmh - max_speed_increase:
                    traction_on() # full traction
                else:
                    traction_on() # fine traction
                    time.sleep(0.05)
                    traction_off()
            else:
                speed_diff = norm_speed_kmh - max_speed_kmh
                if speed_diff > max_speed_increase:
                    max_speed_increase = speed_diff
                traction_off()
        else:
            traction_on()


def forward():
    global is_forward
    is_forward = True


def backward():
    global is_forward
    is_forward = False


def traction_on():
    global is_forward
    if is_forward is True:
        Command.stop_backward()
        Command.start_forward()
    else:
        Command.stop_forward()
        Command.start_backward()


def traction_off():
    Command.reset_traction()


def set_max_speed(speed_kmh):
    global max_speed_kmh
    max_speed_kmh = speed_kmh
