import datetime
import math
import subprocess
import sys
import threading

import Config
import Event

started = False
position = None
rotation = None
speed = None
rotation_speed = None
lock = threading.Lock()


def init():
    args = [sys.argv[1]]

    if 'map' in Config.config:
        args.append('-map')
        args.append(Config.config['map'])

    if 'position' in Config.config:
        args.append('-pos')
        args.append(Config.config['position'])

    if 'rotation' in Config.config:
        args.append('-rot')
        args.append(Config.config['rotation'])

    if 'truck' in Config.config:
        args.append('-truck')
        args.append(Config.config['truck'])

    if 'enter' in Config.config:
        args.append('-enter')

    cmd = subprocess.Popen(args, stdout=subprocess.PIPE)

    thread = threading.Thread(target=read_stdin, args=(cmd.stdout,))
    thread.start()


def read_stdin(ror_input):
    previous_position = [0.0, 0.0, 0.0]
    previous_rotation = [0.0, 0.0, 0.0]
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
                    global rotation_speed
                    lock.acquire()
                    position = [float(numeric_value[0]), float(numeric_value[1]), float(numeric_value[2])]
                    rotation = [float(numeric_value[3]), float(numeric_value[4]), float(numeric_value[5])]
                    global started
                    if started is False:
                        previous_position = position
                        previous_rotation = rotation
                        speed = [0.0, 0.0, 0.0]
                        rotation_speed = [0.0, 0.0, 0.0]
                        started = True
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
                else:
                    print(line)

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


def is_started():
    global started
    return started


def reset():
    global started
    global lock
    global speed
    global rotation_speed
    lock.acquire()
    started = False
    speed = [0.0, 0.0, 0.0]
    rotation_speed = [0.0, 0.0, 0.0]
    lock.release()
