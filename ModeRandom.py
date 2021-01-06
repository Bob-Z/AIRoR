import time
import datetime
import random
import Command
import Input

date_traction = None
date_direction = None
slow_speed = False
previous_slow_speed = False


def init():
    global date_traction
    global date_direction
    global slow_speed
    global previous_slow_speed

    date_traction = datetime.datetime.now()
    date_direction = datetime.datetime.now()
    slow_speed = False
    previous_slow_speed = False


def run():
    global date_traction
    global date_direction
    global slow_speed
    global previous_slow_speed

    if datetime.datetime.now() > date_traction:
        Command.reset_traction()

        traction = random.randrange(3)

        if traction == 0:
            print("Go forward")
            Command.start_forward()
        if traction == 1:
            print("Go forward")
            Command.start_forward()
        if traction == 2:
            print("Go backward")
            Command.start_backward()

        date_traction = datetime.datetime.now() + datetime.timedelta(seconds=random.random() * 10.0)

    if datetime.datetime.now() > date_direction:
        Command.reset_direction()

        direction = random.randrange(3)

        if direction == 0:
            print("Go right")
            Command.start_right()
        elif direction == 1:
            print("Go left")
            Command.start_left()
        else:
            print("Go straight")

        date_direction = datetime.datetime.now() + datetime.timedelta(seconds=random.random() * 10.0)

    speed = Input.get_speed()
    if abs(speed[0]) < 0.05 and abs(speed[1]) < 0.05 and abs(speed[2]) < 0.05:
        print("Slow speed detected")
        slow_speed = True
    else:
        slow_speed = False

    if previous_slow_speed is False and slow_speed is True:
        slow_speed_timestamp = datetime.datetime.now()

    previous_slow_speed = slow_speed

    if slow_speed is True and datetime.datetime.now() > slow_speed_timestamp + datetime.timedelta(seconds=4):
        print("Reset vehicle")
        Command.start_reset_truck()
        time.sleep(0.1)
        Command.stop_reset_truck()
        slow_speed = False
        previous_slow_speed = False

    time.sleep(0.1)
