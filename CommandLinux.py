# https://cgit.freedesktop.org/libevdev/tree/include/linux/linux/input-event-codes.h
# https://readthedocs.org/projects/python-evdev/downloads/pdf/latest/

import os
import time

import libevdev

# fake_keyboard_device = None
fake_joystick_device = None
# fake_keyboard_uinput = None
fake_joystick_uinput = None

input_map = "; -------------------------------------------\n\
; AIRoR fake joystick Input Map\n\
; Created by Bob Zed\n\
; Version 1.1\n\
\n\
; AIRPLANE\n\
;;;AIRPLANE_ELEVATOR_UP           JoystickAxis         0 1 UPPER\n\
;;;AIRPLANE_ELEVATOR_DOWN         JoystickAxis         0 2 UPPER\n\
;AIRPLANE_PARKING_BRAKE         JoystickButton       0 5\n\
;AIRPLANE_REVERSE               JoystickButton       0 4\n\
AIRPLANE_RUDDER_LEFT           JoystickAxis         0 0 LOWER\n\
AIRPLANE_RUDDER_RIGHT          JoystickAxis         0 0 UPPER\n\
;AIRPLANE_STEER_LEFT            JoystickAxis         0 0 LOWER+DEADZONE=0.15\n\
;AIRPLANE_STEER_RIGHT           JoystickAxis         0 0 UPPER+DEADZONE=0.15\n\
;AIRPLANE_THROTTLE_AXIS         None\n\
;AIRPLANE_THROTTLE_UP           JoystickPov          0 0 North\n\
;AIRPLANE_THROTTLE_FULL         JoystickButton       0 2\n\
;AIRPLANE_THROTTLE_NO           JoystickButton       0 1\n\
;AIRPLANE_THROTTLE_DOWN         JoystickPov          0 0 South\n\
;AIRPLANE_TOGGLE_ENGINES        JoystickButton       0 0\n\
\n\
; BOAT\n\
BOAT_STEER_LEFT               JoystickAxis         0 0 LOWER\n\
BOAT_STEER_RIGHT              JoystickAxis         0 0 UPPER\n\
BOAT_THROTTLE_UP              JoystickAxis         0 1 UPPER\n\
BOAT_THROTTLE_DOWN            JoystickAxis         0 2 UPPER\n\
;BOAT_REVERSE                  JoystickButton       0 3\n\
BOAT_CENTER_RUDDER            JoystickButton       0 3\n\
\n\
; CAMERA\n\
;CAMERA_CHANGE                  JoystickButton       0 6\n\
;CAMERA_ROTATE_DOWN             JoystickAxis         0 4 UPPER\n\
;CAMERA_ROTATE_UP               JoystickAxis         0 4 LOWER\n\
;CAMERA_ROTATE_LEFT             JoystickAxis         0 3 LOWER\n\
;CAMERA_ROTATE_RIGHT            JoystickAxis         0 3 UPPER\n\
\n\
; CHARACTER\n\
CHARACTER_BACKWARDS            JoystickAxis         0 1 UPPER\n\
CHARACTER_FORWARD              JoystickAxis         0 1 LOWER\n\
CHARACTER_JUMP                 JoystickButton       0 0\n\
CHARACTER_LEFT                 JoystickAxis         0 0 LOWER\n\
CHARACTER_RIGHT                JoystickAxis         0 0 UPPER\n\
CHARACTER_RUN                  JoystickButton       0 0\n\
\n\
; COMMON\n\
;COMMON_ENTER_OR_EXIT_TRUCK     JoystickButton       0 3\n\
;COMMON_LOCK                    JoystickPov          0 0 North\n\
;COMMON_QUIT_GAME               JoystickButton       0 7\n\
;COMMON_TOGGLE_TRUCK_LIGHTS     JoystickPov          0 0 West\n\
COMMON_OUTPUT_POSITION         JoystickButton       0 1\n\
COMMON_RESET_TRUCK             JoystickButton       0 2\n\
\n\
; TRUCK\n\
TRUCK_ACCELERATE               JoystickAxis         0 1 UPPER\n\
TRUCK_BRAKE                    JoystickAxis         0 2 UPPER\n\
;TRUCK_AUTOSHIFT_UP             JoystickPov          0 0 North\n\
;TRUCK_AUTOSHIFT_DOWN           JoystickPov          0 0 South\n\
;TRUCK_HORN                     JoystickButton       0 8\n\
;TRUCK_PARKING_BRAKE            JoystickButton       0 5\n\
TRUCK_AUTOSHIFT_DOWN               JoystickButton       0 3\n\
TRUCK_AUTOSHIFT_UP                 JoystickButton       0 4\n\
;TRUCK_SHIFT_DOWN               JoystickButton       0 3\n\
;TRUCK_SHIFT_UP                 JoystickButton       0 4\n\
;TRUCK_MANUAL_CLUTCH                       JoystickButton       0 4\n\
;TRUCK_STARTER                  JoystickButton       0 0\n\
TRUCK_STEER_LEFT               JoystickAxis         0 0 LOWER\n\
TRUCK_STEER_RIGHT              JoystickAxis         0 0 UPPER\n\
;TRUCK_TOGGLE_CONTACT           JoystickButton       0 9\n\
\n\
; COMMANDS\n\
COMMANDS_01                    JoystickButton       0 5\n\
COMMANDS_02                    JoystickButton       0 6\n\
"


def install_input_file():
    filename = os.getenv("HOME") + "/.rigsofrods/config/AIRoR_fake_joystick_device.map"

    input_map_file = open(filename, 'w')
    input_map_file.write(input_map)
    input_map_file.close()


def init():
    install_input_file()

    # global fake_keyboard_device
    global fake_joystick_device
    # global fake_keyboard_uinput
    global fake_joystick_uinput

    # fake_keyboard_device = libevdev.Device()
    # fake_keyboard_device.name = 'AIRoR fake keyboard device'
    # fake_keyboard_device.enable(libevdev.EV_KEY.KEY_UP)
    # fake_keyboard_device.enable(libevdev.EV_KEY.KEY_DOWN)
    # fake_keyboard_device.enable(libevdev.EV_KEY.KEY_RIGHT)
    # fake_keyboard_device.enable(libevdev.EV_KEY.KEY_LEFT)
    # fake_keyboard_device.enable(libevdev.EV_KEY.KEY_PAUSE)
    # fake_keyboard_device.enable(libevdev.EV_KEY.KEY_I)

    # fake_keyboard_uinput = fake_keyboard_device.create_uinput_device()

    fake_joystick_device = libevdev.Device()
    fake_joystick_device.name = 'AIRoR fake joystick device'

    # This is needed to be identified by OIS as a joystick
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_TRIGGER)

    fake_joystick_device.enable(libevdev.EV_ABS.ABS_X, libevdev.InputAbsInfo(minimum=-100, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_Y, libevdev.InputAbsInfo(minimum=0, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_Z, libevdev.InputAbsInfo(minimum=0, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_RX, libevdev.InputAbsInfo(minimum=0, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_RY, libevdev.InputAbsInfo(minimum=0, maximum=100))
    fake_joystick_device.enable(libevdev.EV_ABS.ABS_RZ, libevdev.InputAbsInfo(minimum=0, maximum=100))
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_SOUTH)
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_EAST)
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_NORTH)
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_WEST)
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_Z)
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_TL)
    fake_joystick_device.enable(libevdev.EV_KEY.BTN_TR)
    # fake_joystick_device.enable(libevdev.EV_ABS.ABS_RX, absinfo)
    # fake_joystick_device.enable(libevdev.EV_ABS.ABS_RY, absinfo)
    # fake_joystick_device.enable(libevdev.EV_ABS.ABS_RZ, absinfo)

    fake_joystick_uinput = fake_joystick_device.create_uinput_device()

    # init time
    time.sleep(1)

    # print('fake keyboard device is now at {}'.format(fake_keyboard_uinput.devnode))
    print('fake joystick device is now at {}'.format(fake_joystick_uinput.devnode))


def reset_direction():
    analog(libevdev.EV_ABS.ABS_X, 0)


def analog(key, value_in):
    global fake_joystick_uinput
    analog = [libevdev.InputEvent(key, value=value_in),
              libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_joystick_uinput.send_events(analog)


def keyboard_press(key):
    global fake_keyboard_uinput
    press = [libevdev.InputEvent(key, value=1),
             libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_keyboard_uinput.send_events(press)


def keyboard_release(key):
    global fake_keyboard_uinput
    release = [libevdev.InputEvent(key, value=0),
               libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_keyboard_uinput.send_events(release)


def joy_press(key):
    global fake_joystick_uinput
    press = [libevdev.InputEvent(key, value=1),
             libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_joystick_uinput.send_events(press)


def joy_release(key):
    global fake_joystick_uinput
    release = [libevdev.InputEvent(key, value=0),
               libevdev.InputEvent(libevdev.EV_SYN.SYN_REPORT, value=0)]
    fake_joystick_uinput.send_events(release)


def TRUCK_ACCELERATE(value=100):
    # print("Accelerate " + str(value))
    analog(libevdev.EV_ABS.ABS_Y, min(int(abs(value)), 100))


def TRUCK_BRAKE(value=100):
    # print("Brake " + str(value))
    analog(libevdev.EV_ABS.ABS_Z, min(int(abs(value)), 100))


def TRUCK_STEER_LEFT(value=100):
    analog(libevdev.EV_ABS.ABS_X, -(min(int(abs(value)), 100)))


def TRUCK_STEER_RIGHT(value=100):
    analog(libevdev.EV_ABS.ABS_X, (min(int(abs(value)), 100)))


def set_TRUCK_STEER(value):
    analog(libevdev.EV_ABS.ABS_X, value)


def start_COMMON_OUTPUT_POSITION():
    # print("start_COMMON_OUTPUT_POSITION")
    joy_press(libevdev.EV_KEY.BTN_SOUTH)


def stop_COMMON_OUTPUT_POSITION():
    # print("stop_COMMON_OUTPUT_POSITION")
    joy_release(libevdev.EV_KEY.BTN_SOUTH)


def start_COMMON_RESET_TRUCK():
    joy_press(libevdev.EV_KEY.BTN_EAST)


def stop_COMMON_RESET_TRUCK():
    joy_release(libevdev.EV_KEY.BTN_EAST)


def BOAT_STEER_LEFT(value=100):
    TRUCK_STEER_LEFT(value)


def BOAT_STEER_RIGHT(value=100):
    TRUCK_STEER_RIGHT(value)


def start_BOAT_CENTER_RUDDER():
    # print("start_center_rudder")
    joy_press(libevdev.EV_KEY.BTN_NORTH)


def stop_BOAT_CENTER_RUDDER():
    # print("stop_center_rudder")
    joy_release(libevdev.EV_KEY.BTN_NORTH)


def start_COMMANDS_01():
    # print("start_command_1")
    joy_press(libevdev.EV_KEY.BTN_WEST)


def stop_COMMANDS_01():
    # print("stop_command_1")
    joy_release(libevdev.EV_KEY.BTN_WEST)


def start_COMMANDS_02():
    # print("start_command_2")
    joy_press(libevdev.EV_KEY.BTN_Z)


def stop_COMMANDS_02():
    # print("stop_command_2")
    joy_release(libevdev.EV_KEY.BTN_Z)


def start_AUTOSHIFT_DOWN():
    #print("start_autoshift_down")
    joy_press(libevdev.EV_KEY.BTN_NORTH)


def stop_AUTOSHIFT_DOWN():
    #print("stop_autoshift_down")
    joy_release(libevdev.EV_KEY.BTN_NORTH)


def start_AUTOSHIFT_UP():
    # print("start_autoshift_up")
    joy_press(libevdev.EV_KEY.BTN_TR)


def stop_AUTOSHIFT_UP():
    # print("stop_autoshift_up")
    joy_release(libevdev.EV_KEY.BTN_TR)
