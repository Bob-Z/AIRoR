import math

import Command
import Event
import Input
import Traction
import Config
import numpy


waypoint = None
event_ahead_qty = 1


def init():
    global waypoint
    waypoint = Config.config['waypoint']


def run():
    print("Mode truck waypoint: " + str(len(waypoint)) + " waypoints")
    Traction.forward()

    current_waypoint = 0
    if waypoint[current_waypoint][3] != -1:
        Traction.set_max_speed(waypoint[current_waypoint][3])
    print("max speed ", waypoint[current_waypoint][3])

    prev_rotation = [0.0, 0.0, 0.0]

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

        rotation_since_previous_event = prev_rotation[1] - rotation[1]
        global event_ahead_qty
        next_diff_rot = rotation[1] - (event_ahead_qty * rotation_since_previous_event) - target_angle

        prev_rotation = rotation

        if next_diff_rot > 180.0:
            next_diff_rot = next_diff_rot - 360.0
        if next_diff_rot < -180.0:
            next_diff_rot = 360.0 + next_diff_rot
        # print("diff_rot = ", diff_rot)

        # wheel_force = max(5, abs(diff_rot) * 1.5)
        wheel_force = 10 + abs(next_diff_rot)
        # print("wheel force: ", wheel_force)

        if next_diff_rot > 0.0:
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
    v0 = numpy.array(p0) - numpy.array(p1)
    v1 = numpy.array(p2) - numpy.array(p1)

    angle = numpy.math.atan2(numpy.linalg.det([v0, v1]), numpy.dot(v0, v1))
    return numpy.degrees(angle)


def check_waypoint_distance(current_waypoint, position, speed):
    global waypoint
    dist_x = position[0] - waypoint[current_waypoint][0]
    dist_y = position[2] - waypoint[current_waypoint][2]
    distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
    # print("distance: ", distance)

    speed = Input.get_norm_speed()
    proximity_distance = speed * 0.5  # distance in 0.5 seconds
    if proximity_distance < 2.0:
        proximity_distance = 2.0

    if distance < proximity_distance:
        new_waypoint = (current_waypoint + 1) % len(waypoint)
        print("next waypoint ", new_waypoint)
        if waypoint[new_waypoint][3] != -1:
            Traction.set_max_speed(waypoint[new_waypoint][3])
            print("max speed ", waypoint[new_waypoint][3])

        if waypoint[current_waypoint][4] >= 0:
            global event_ahead_qty
            event_ahead_qty = waypoint[current_waypoint][4]

        return new_waypoint

    return current_waypoint
