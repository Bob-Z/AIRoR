import datetime
import math
import os
import subprocess
import sys
import threading

import Event

started = False
position = None
rotation = None
speed = None
lock = threading.Lock()

input_map = "; -------------------------------------------\n\
; AIRoR fake joystick Input Map\n\
; Created by Bob Zed\n\
; Version 1.1\n\
\n\
; AIRPLANE\n\
AIRPLANE_ELEVATOR_DOWN         JoystickAxis         0 1 UPPER\n\
AIRPLANE_ELEVATOR_UP           JoystickAxis         0 1 LOWER\n\
AIRPLANE_PARKING_BRAKE         JoystickButton       0 5\n\
AIRPLANE_REVERSE               JoystickButton       0 4\n\
AIRPLANE_RUDDER_LEFT           JoystickAxis         0 5 UPPER\n\
AIRPLANE_RUDDER_RIGHT          JoystickAxis         0 2 UPPER\n\
AIRPLANE_STEER_LEFT            JoystickAxis         0 0 LOWER+DEADZONE=0.15\n\
AIRPLANE_STEER_RIGHT           JoystickAxis         0 0 UPPER+DEADZONE=0.15\n\
AIRPLANE_THROTTLE_AXIS         None\n\
AIRPLANE_THROTTLE_UP           JoystickPov          0 0 North\n\
AIRPLANE_THROTTLE_FULL         JoystickButton       0 2\n\
AIRPLANE_THROTTLE_NO           JoystickButton       0 1\n\
AIRPLANE_THROTTLE_DOWN         JoystickPov          0 0 South\n\
AIRPLANE_TOGGLE_ENGINES        JoystickButton       0 0\n\
\n\
; BOAT\n\
BOAT_STEER_LEFT               JoystickAxis         0 0 LOWER\n\
BOAT_STEER_RIGHT              JoystickAxis         0 0 UPPER\n\
BOAT_THROTTLE_UP              JoystickAxis         0 1 UPPER\n\
BOAT_THROTTLE_DOWN            JoystickAxis         0 2 UPPER\n\
;BOAT_REVERSE                  JoystickButton       0 3\n\
BOAT_CENTER_RUDDER            JoystickButton       0 2\n\
\n\
; CAMERA\n\
CAMERA_CHANGE                  JoystickButton       0 6\n\
CAMERA_ROTATE_DOWN             JoystickAxis         0 4 UPPER\n\
CAMERA_ROTATE_UP               JoystickAxis         0 4 LOWER\n\
CAMERA_ROTATE_LEFT             JoystickAxis         0 3 LOWER\n\
CAMERA_ROTATE_RIGHT            JoystickAxis         0 3 UPPER\n\
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
\n\
; TRUCK\n\
TRUCK_ACCELERATE               JoystickAxis         0 1 UPPER\n\
;TRUCK_AUTOSHIFT_UP             JoystickPov          0 0 North\n\
;TRUCK_AUTOSHIFT_DOWN           JoystickPov          0 0 South\n\
TRUCK_BRAKE                    JoystickAxis         0 2 UPPER\n\
;TRUCK_HORN                     JoystickButton       0 8\n\
;TRUCK_PARKING_BRAKE            JoystickButton       0 5\n\
;TRUCK_SHIFT_DOWN               JoystickButton       0 1\n\
;TRUCK_SHIFT_UP                 JoystickButton       0 2\n\
;TRUCK_MANUAL_CLUTCH                       JoystickButton       0 4\n\
;TRUCK_STARTER                  JoystickButton       0 0\n\
TRUCK_STEER_LEFT               JoystickAxis         0 0 LOWER\n\
TRUCK_STEER_RIGHT              JoystickAxis         0 0 UPPER\n\
;TRUCK_TOGGLE_CONTACT           JoystickButton       0 9\n\
"


def install_input_file():
    filename = os.getenv("HOME") + "/.rigsofrods/config/AIRoR_fake_joystick_device.map"

    input_map_file = open(filename, 'w')
    input_map_file.write(input_map)
    input_map_file.close()


def init():
    install_input_file()

    cmd = subprocess.Popen([sys.argv[1]], shell=True, stdout=subprocess.PIPE)

    thread = threading.Thread(target=read_stdin, args=(cmd.stdout,))
    thread.start()


def read_stdin(ror_input):
    previous_position = [0.0, 0.0, 0.0]
    previous_timestamp = datetime.datetime.now()
    while True:
        try:
            for byte_array_line in ror_input:
                line = byte_array_line.decode('utf-8')
                if line[0:9] == "Position:":
                    timestamp = datetime.datetime.now()
                    stripped = line.replace('\x1b[0m\n', '').replace(' ', '')
                    data = stripped.split(':')
                    numeric_value = data[1].split(',')
                    global position
                    global rotation
                    global speed
                    lock.acquire()
                    position = [float(numeric_value[0]), float(numeric_value[1]), float(numeric_value[2])]
                    rotation = [float(numeric_value[3]), float(numeric_value[4]), float(numeric_value[5])]
                    global started
                    if started is False:
                        previous_position = position
                        speed = [0.0, 0.0, 0.0]
                        started = True
                    else:
                        duration = timestamp - previous_timestamp
                        # print("duration", duration.total_seconds())
                        for i in range(3):
                            speed[i] = (position[i] - previous_position[i]) / duration.total_seconds()

                        previous_timestamp = timestamp
                        previous_position = position
                    lock.release()

                    Event.set_event()
                    Event.clear_event()

                    # print("pos", position)
                    # print("rot", rotation)
                    # print("spd", speed)

                # print(line, end='')
        except UnicodeDecodeError:
            print("UnicodeDecodeError exception")


def get_position():
    global lock
    global position
    lock.acquire()
    ret_position = position
    lock.release()

    return ret_position


def get_rotation():
    global lock
    global rotation
    lock.acquire()
    ret_rotation = rotation
    lock.release()

    return ret_rotation


def get_speed():
    global lock
    global speed
    lock.acquire()
    ret_speed = speed
    lock.release()

    return ret_speed


def get_norm_speed():
    global speed
    return math.sqrt(speed[0] * speed[0] + speed[1] * speed[1] + speed[2] * speed[2])


def is_started():
    global started
    return started
