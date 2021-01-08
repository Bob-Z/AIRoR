import time
import datetime
import random
import Command
import Input
import Traction

date_traction = None
date_direction = None
slow_speed = False
previous_slow_speed = False
slow_speed_timestamp = None


def init():
    global date_traction
    global date_direction
    global slow_speed
    global previous_slow_speed
    global slow_speed_timestamp

    date_traction = datetime.datetime.now()
    date_direction = datetime.datetime.now()
    slow_speed = False
    previous_slow_speed = False
    slow_speed_timestamp = datetime.datetime.now()


def run():
    while True:
        global slow_speed
        global previous_slow_speed

        manage_traction()

        #manage_direction()

        manage_reset()

        time.sleep(0.01)


def manage_traction():
    global date_traction

    if datetime.datetime.now() > date_traction:
        rand = random.randrange(3)
        if rand == 0 or rand == 1:
            print("Go forward")
            Traction.forward()
        if rand == 2:
            print("Go backward")
            #Traction.backward()
            Traction.forward()

        date_traction = datetime.datetime.now() + datetime.timedelta(seconds=random.random() * 10.0)


def manage_direction():
    global date_direction

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


def manage_reset():
    global slow_speed
    global previous_slow_speed
    global slow_speed_timestamp

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
