import math

import numpy as np

import Command
import Event
import Input
import Traction
import Config


waypoint = None


def init():
    global waypoint
    waypoint = Config.config['waypoint']


def run():
    Traction.forward()

    current_waypoint = 0
    if waypoint[current_waypoint][3] != -1:
        Traction.set_max_speed(waypoint[current_waypoint][3])
    print("max speed ", waypoint[current_waypoint][3])

    while True:
        Event.wait()

        position = Input.get_position()
        rotation = Input.get_rotation()
        speed = Input.get_speed()

        current_waypoint = check_waypoint_distance(current_waypoint, position, speed)

        waypoint_angle = calc_angle([position[0], position[2] + 1.0], [position[0], position[2]],
                                    [waypoint[current_waypoint][0], waypoint[current_waypoint][2]])

        if waypoint_angle > 0:
            target_angle = waypoint_angle - 180.0
        else:
            target_angle = waypoint_angle + 180.0
        # print('target_angle: ', target_angle)
        # print('rotation:', rotation)

        diff_rot = rotation[1] - target_angle
        # print('rotation[1] - target_angle:', diff_rot)

        if diff_rot > 180.0:
            diff_rot = diff_rot - 360.0
        if diff_rot < -180.0:
            diff_rot = 360.0 + diff_rot
        # print("diff_rot = ", diff_rot)

        # wheel_force = max(5, abs(diff_rot) * 1.5)
        wheel_force = 10 + abs(diff_rot)
        # print("wheel force: ", wheel_force)

        if diff_rot > 0.0:
            # print("left")
            Command.start_left(wheel_force)
        else:
            # print("right")
            Command.start_right(wheel_force)


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


def check_waypoint_distance(current_waypoint, position, speed):
    global waypoint
    dist_x = position[0] - waypoint[current_waypoint][0]
    dist_y = position[2] - waypoint[current_waypoint][2]
    distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
    # print("distance: ", distance)

    speed = Input.get_norm_speed()
    proximity_distance = speed * 0.5  # distance in 0.5 seconds

    if distance < proximity_distance:
        new_waypoint = (current_waypoint + 1) % len(waypoint)
        print("next waypoint ", new_waypoint)
        if waypoint[new_waypoint][3] != -1:
            Traction.set_max_speed(waypoint[new_waypoint][3])
            print("max speed ", waypoint[new_waypoint][3])

        return new_waypoint

    return current_waypoint
