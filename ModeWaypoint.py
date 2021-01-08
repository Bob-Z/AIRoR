import time

import numpy as np

import Input
import Command
import Traction
import Event

waypoint = [512.0, 0.0, 512.0]
waypoint = [412.0, 0.0, 512.0]


def init():
    pass


def run():
    Traction.forward()
    while True:
        Event.wait()

        position = Input.get_position()
        rotation = Input.get_rotation()
        waypoint_angle = calc_angle([position[0], position[2] + 1.0], [position[0], position[2]], [waypoint[0], waypoint[2]])

        if waypoint_angle > 0:
            target_angle = waypoint_angle - 180.0
        else:
            target_angle = waypoint_angle + 180.0
        print('target_angle: ', target_angle)
        print('rotation:', rotation)

        diff_rot = rotation[1] - target_angle
        print('rotation[1] - target_angle:', diff_rot)

        if abs(diff_rot) > 20.0:
            if diff_rot > 0.0:
                if diff_rot < 180.0:
                    Command.reset_direction()
                    Command.start_left()
                else:
                    Command.reset_direction()
                    Command.start_right()
            else:
                if diff_rot < -180.0:
                    Command.reset_direction()
                    Command.start_left()
                else:
                    Command.reset_direction()
                    Command.start_right()
        elif abs(diff_rot) > 5:
            if diff_rot > 0.0:
                if diff_rot < 180.0:
                    Command.start_left()
                    time.sleep(0.01)
                    Command.reset_direction()
                else:
                    Command.start_right()
                    time.sleep(0.01)
                    Command.reset_direction()
            else:
                if diff_rot < -180.0:
                    Command.start_left()
                    time.sleep(0.01)
                    Command.reset_direction()
                else:
                    Command.start_right()
                    time.sleep(0.01)
                    Command.reset_direction()


''' 
compute angle (in degrees) for p0p1p2 corner
Inputs:
    p0,p1,p2 - points in the form of [x,y]
'''


def calc_angle(p0, p1, p2):
    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    return np.degrees(angle)
