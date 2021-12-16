# https://cgit.freedesktop.org/libevdev/tree/include/posix/posix/input-event-codes.h
# https://readthedocs.org/projects/python-evdev/downloads/pdf/latest/

import os

if os.name == 'posix':
    import CommandLinux


def init():
    print("OS: ", os.name)
    if os.name == 'posix':
        CommandLinux.init()


def TRUCK_ACCELERATE(value=100):
    if os.name == 'posix':
        CommandLinux.TRUCK_ACCELERATE(value)


def TRUCK_BRAKE(value=100):
    if os.name == 'posix':
        CommandLinux.TRUCK_BRAKE(value)


def TRUCK_STEER_LEFT(value=100):
    if os.name == 'posix':
        CommandLinux.TRUCK_STEER_LEFT(value)


def TRUCK_STEER_RIGHT(value=100):
    if os.name == 'posix':
        CommandLinux.TRUCK_STEER_RIGHT(value)


def set_TRUCK_STEER(value_in):
    value = int(value_in)
    if value > 100:
        value = 100
    if value < -100:
        value = -100

    if os.name == 'posix':
        CommandLinux.set_TRUCK_STEER(value)


def start_COMMON_OUTPUT_POSITION():
    if os.name == 'posix':
        CommandLinux.start_COMMON_OUTPUT_POSITION()


def stop_COMMON_OUTPUT_POSITION():
    if os.name == 'posix':
        CommandLinux.stop_COMMON_OUTPUT_POSITION()


def start_COMMON_RESET_TRUCK():
    if os.name == 'posix':
        CommandLinux.start_COMMON_RESET_TRUCK()


def stop_COMMON_RESET_TRUCK():
    if os.name == 'posix':
        CommandLinux.stop_COMMON_RESET_TRUCK()


def BOAT_STEER_LEFT(value=100):
    if os.name == 'posix':
        CommandLinux.BOAT_STEER_LEFT(value)


def BOAT_STEER_RIGHT(value=100):
    if os.name == 'posix':
        CommandLinux.BOAT_STEER_RIGHT(value)


def start_BOAT_CENTER_RUDDER():
    if os.name == 'posix':
        CommandLinux.start_BOAT_CENTER_RUDDER()


def stop_BOAT_CENTER_RUDDER():
    if os.name == 'posix':
        CommandLinux.stop_BOAT_CENTER_RUDDER()


def start_COMMANDS_01():
    if os.name == 'posix':
        CommandLinux.start_COMMANDS_01()


def stop_COMMANDS_01():
    if os.name == 'posix':
        CommandLinux.stop_COMMANDS_01()


def start_COMMANDS_02():
    if os.name == 'posix':
        CommandLinux.start_COMMANDS_02()


def stop_COMMANDS_02():
    if os.name == 'posix':
        CommandLinux.stop_COMMANDS_02()


def start_AUTOSHIFT_DOWN():
    if os.name == 'posix':
        CommandLinux.start_AUTOSHIFT_DOWN()


def stop_AUTOSHIFT_DOWN():
    if os.name == 'posix':
        CommandLinux.stop_AUTOSHIFT_DOWN()


def start_AUTOSHIFT_UP():
    if os.name == 'posix':
        CommandLinux.start_AUTOSHIFT_UP()


def stop_SHIFT_UP():
    if os.name == 'posix':
        CommandLinux.stop_AUTOSHIFT_UP()
