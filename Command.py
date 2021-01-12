# https://cgit.freedesktop.org/libevdev/tree/include/linux/linux/input-event-codes.h
# https://readthedocs.org/projects/python-evdev/downloads/pdf/latest/

import time

import libevdev

fake_keyboard_device = None
fake_joystick_device = None
fake_keyboard_uinput = None
fake_joystick_uinput = None


def init():
    global fake_keyboard_device
    global fake_joystick_device
    global fake_keyboard_uinput
    global fake_joystick_uinput

    fake_keyboard_device = libevdev.Device()
    fake_keyboard_device.name = 'AIRoR fake keyboard device'
    fake_keyboard_device.enable(libevdev.EV_KEY.KEY_UP)
    fake_keyboard_device.enable(libevdev.EV_KEY.KEY_DOWN)
    fake_keyboard_device.enable(libevdev.EV_KEY.KEY_RIGHT)
    fake_keyboard_device.enable(libevdev.EV_KEY.KEY_LEFT)
    fake_keyboard_device.enable(libevdev.EV_KEY.KEY_PAUSE)
    fake_keyboard_device.enable(libevdev.EV_KEY.KEY_I)

    fake_keyboard_uinput = fake_keyboard_device.create_uinput_device()

    fake_joystick_device = libevdev.Device()
    fake_joystick_device.name = 'AIRoR fake joystick device'

    # This is needed to be identified by OIS as a joystick
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_TRIGGER)

    fake_joystick_device.enable(libevdev.EV_ABS.ABS_X, libevdev.InputAbsInfo(minimum=-100, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_Y, libevdev.InputAbsInfo(minimum=0, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_Z, libevdev.InputAbsInfo(minimum=0, maximum=100))
    #fake_joystick_device.enable(libevdev.EV_ABS.ABS_RX, absinfo)
    #fake_joystick_device.enable(libevdev.EV_ABS.ABS_RY, absinfo)
    #fake_joystick_device.enable(libevdev.EV_ABS.ABS_RZ, absinfo)

    fake_joystick_uinput = fake_joystick_device.create_uinput_device()

    # init time
    time.sleep(1)

    print('fake keyboard device is now at {}'.format(fake_keyboard_uinput.devnode))
    print('fake joystick device is now at {}'.format(fake_joystick_uinput.devnode))


def reset_direction():
    analog(libevdev.EV_ABS.ABS_X, 0)


def analog(key, value_in):
    global fake_joystick_uinput
    analog = [libevdev.InputEvent(key, value=value_in),
              libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_joystick_uinput.send_events(analog)


def press(key):
    global fake_keyboard_uinput
    press = [libevdev.InputEvent(key, value=1),
             libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_keyboard_uinput.send_events(press)


def release(key):
    global fake_keyboard_uinput
    release = [libevdev.InputEvent(key, value=0),
               libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_keyboard_uinput.send_events(release)


def accelerate(value=100):
    analog(libevdev.EV_ABS.ABS_Y, min(int(abs(value)), 100))


def brake(value=100):
    analog(libevdev.EV_ABS.ABS_Z, min(int(abs(value)), 100))


def start_left(value=100):
    analog(libevdev.EV_ABS.ABS_X, -(min(int(abs(value)), 100)))


def stop_left():
    analog(libevdev.EV_ABS.ABS_X, 0)


def start_right(value=100):
    analog(libevdev.EV_ABS.ABS_X, (min(int(abs(value)), 100)))


def stop_right():
    analog(libevdev.EV_ABS.ABS_X, 0)


def set_wheel(value_in):
    value = int(value_in)
    if value > 100:
        value = 100
    if value < -100:
        value = -100

    analog(libevdev.EV_ABS.ABS_X, value)


def start_get_position():
    press(libevdev.EV_KEY.KEY_PAUSE)


def stop_get_position():
    release(libevdev.EV_KEY.KEY_PAUSE)


def start_reset_truck():
    press(libevdev.EV_KEY.KEY_I)


def stop_reset_truck():
    release(libevdev.EV_KEY.KEY_I)
