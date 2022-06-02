import datetime
import math
import os
import subprocess
import sys
import time
import threading

import Config
import Command
import Event

first_data = True
position = None
rotation = None
speed = None
rotation_speed = None
lock = threading.Lock()
is_pushing = False
force_reset = False
log_file = open("position.txt", "w")

def init():
    args = [sys.argv[1]]

    if 'map' in Config.config_json:
        args.append('-map')
        args.append(Config.config_json['map'])

    if 'position' in Config.config_json:
        args.append('-pos')
        args.append(Config.config_json['position'])

    if 'rotation' in Config.config_json:
        args.append('-rot')
        args.append(Config.config_json['rotation'])

    if 'truck' in Config.config_json:
        args.append('-truck')
        args.append(Config.config_json['truck'])

    if 'enter' in Config.config_json:
        args.append('-enter')

    cmd = subprocess.Popen(args, stdout=subprocess.PIPE)

    thread = threading.Thread(target=read_stdin, args=(cmd.stdout,))
    thread.start()

    thread_push = threading.Thread(target=push_position_button)
    thread_push.start()


def read_stdin(ror_input):
    previous_position = [0.0, 0.0, 0.0]
    previous_rotation = [0.0, 0.0, 0.0]
    previous_timestamp = datetime.datetime.now()

    global log_file

    while True:
        try:
            for byte_array_line in ror_input:
                line = byte_array_line.decode('utf-8')
                if line[0:9] == "Position:":
                    log_file.write(line)

                    timestamp = datetime.datetime.now()
                    stripped = line.replace('\x1b[0m\n', '').replace(' ', '')
                    data = stripped.split(':')
                    numeric_value = data[1].split(',')
                    global position
                    global rotation
                    global speed
                    global rotation_speed
                    lock.acquire()
                    position = [float(numeric_value[0]), float(numeric_value[1]), float(numeric_value[2])]
                    rotation = [float(numeric_value[3]), float(numeric_value[4]), float(numeric_value[5])]
                    global first_data
                    if first_data is True:
                        previous_position = position
                        previous_rotation = rotation
                        speed = [0.0, 0.0, 0.0]
                        rotation_speed = [0.0, 0.0, 0.0]
                        first_data = False

                        global is_pushing
                        if is_pushing is False:
                            is_pushing = True
                    else:
                        duration = timestamp - previous_timestamp
                        # print("duration", duration.total_seconds())
                        for i in range(3):
                            speed[i] = (position[i] - previous_position[i]) / duration.total_seconds()
                            rotation_speed[i] = (rotation[i] - previous_rotation[i]) / duration.total_seconds()

                        previous_timestamp = timestamp
                        previous_position = position
                    lock.release()

                    Event.set_event()
                    Event.clear_event()

                    # print("pos", position)
                    # print("rot", rotation)
                    # print("spd", speed)

                elif line[0:49] == "[RoR|CVar]             sim_state:  \"2\" (was: \"1\")":
                    is_pushing = False
                    print(line, end='')
                    print("AIRoR paused")
                elif line[0:49] == "[RoR|CVar]             sim_state:  \"1\" (was: \"2\")":
                    print(line, end='')
                    global force_reset
                    force_reset = True

                    Command.start_COMMON_RESET_TRUCK()
                    time.sleep(0.1)
                    Command.stop_COMMON_RESET_TRUCK()

                    Event.set_event()
                    Event.clear_event()

                    print("AIRoR reset")
                elif line[0:49] == "[RoR|CVar]             app_state:  \"3\" (was: \"2\")":
                    print(line, end='')
                    print("AIRoR exit")

                    log_file.close()

                    os._exit(0)
                else:
                    print(line, end='')

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


def get_speed_norm():
    global speed
    return math.sqrt(speed[0] * speed[0] + speed[1] * speed[1] + speed[2] * speed[2])


def get_rotation_speed():
    global lock
    global rotation_speed
    lock.acquire()
    ret_speed = rotation_speed
    lock.release()

    return ret_speed


def reset():
    global first_data
    global lock
    global speed
    global rotation_speed
    lock.acquire()
    first_data = True
    speed = [0.0, 0.0, 0.0]
    rotation_speed = [0.0, 0.0, 0.0]
    lock.release()


def push_position_button():
    global is_pushing

    while True:
        if is_pushing is False:
            time.sleep(0.1)
        else:
            while is_pushing is True:
                Command.start_COMMON_OUTPUT_POSITION()
                time.sleep(0.05)
                Command.stop_COMMON_OUTPUT_POSITION()
                time.sleep(0.05)


def is_reset_forced():
    global force_reset
    if force_reset is True:
        force_reset = False
        return True
    else:
        return False
