import random
import time
import datetime
import socket
import struct

import libevdev

device = None
uinput = None


def init():
    global device
    global uinput
    device = libevdev.Device()
    device.name = 'RoRBot fake device'
    device.enable(libevdev.EV_KEY.BTN_LEFT)
    device.enable(libevdev.EV_KEY.BTN_MIDDLE)
    device.enable(libevdev.EV_KEY.BTN_RIGHT)
    device.enable(libevdev.EV_KEY.KEY_UP)
    device.enable(libevdev.EV_KEY.KEY_DOWN)
    device.enable(libevdev.EV_KEY.KEY_RIGHT)
    device.enable(libevdev.EV_KEY.KEY_LEFT)
    device.enable(libevdev.EV_KEY.KEY_PAUSE)
    device.enable(libevdev.EV_KEY.KEY_I)

    uinput = device.create_uinput_device()

    # init time
    time.sleep(1)

    #print('device is now at {}'.format(uinput.devnode))


def reset_command():
    reset_traction()
    reset_direction()


def reset_traction():
    stop_forward()
    stop_backward()


def reset_direction():
    stop_left()
    stop_right()


def press(key):
    global uinput
    press = [libevdev.InputEvent(key, value=1),
             libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    uinput.send_events(press)


def release(key):
    global uinput
    release = [libevdev.InputEvent(key, value=0),
             libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    uinput.send_events(release)


def start_forward():
    press(libevdev.EV_KEY.KEY_UP)


def stop_forward():
    release(libevdev.EV_KEY.KEY_UP)


def start_backward():
    press(libevdev.EV_KEY.KEY_DOWN)


def stop_backward():
    release(libevdev.EV_KEY.KEY_DOWN)


def start_left():
    press(libevdev.EV_KEY.KEY_LEFT)


def stop_left():
    release(libevdev.EV_KEY.KEY_LEFT)


def start_right():
    press(libevdev.EV_KEY.KEY_RIGHT)


def stop_right():
    release(libevdev.EV_KEY.KEY_RIGHT)


def start_get_position():
    press(libevdev.EV_KEY.KEY_PAUSE)


def stop_get_position():
    release(libevdev.EV_KEY.KEY_PAUSE)


def start_reset_truck():
    press(libevdev.EV_KEY.KEY_I)


def stop_reset_truck():
    release(libevdev.EV_KEY.KEY_I)
