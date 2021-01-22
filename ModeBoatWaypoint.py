import math

import numpy as np

import Command
import Config
import Event
import Input
import Throttle

waypoint = None
RIGHT = 0
LEFT = 1
CENTER = 2

event_ahead_qty = 1


def init():
    global waypoint
    waypoint = Config.config['waypoint']


def run():
    print("Mode boat waypoint: " + str(len(waypoint)) + " waypoints")
    current_waypoint = 0
    if waypoint[current_waypoint][3] != -1:
        Throttle.set_max_speed(waypoint[current_waypoint][3])
    print("waypoint ", current_waypoint)
    print("max speed ", waypoint[current_waypoint][3])

    prev_rotation = [0.0, 0.0, 0.0]

    direction = CENTER

    while True:
        Event.wait()

        position = Input.get_position()
        rotation = Input.get_rotation()

        current_waypoint = check_waypoint_distance(current_waypoint, position)

        waypoint_angle = calc_angle([position[0], position[2] + 1.0], [position[0], position[2]],
                                    [waypoint[current_waypoint][0], waypoint[current_waypoint][2]])

        if waypoint_angle > 0:
            target_angle = waypoint_angle - 180.0
        else:
            target_angle = waypoint_angle + 180.0

        rotation_since_previous_event = prev_rotation[1] - rotation[1]
        next_diff_rot = rotation[1] - (event_ahead_qty * rotation_since_previous_event) - target_angle

        prev_rotation = rotation

        if next_diff_rot > 180.0:
            next_diff_rot = next_diff_rot - 360.0
        if next_diff_rot < -180.0:
            next_diff_rot = 360.0 + next_diff_rot
        # print("diff_rot = ", diff_rot)

        if next_diff_rot > 1.0:
            # print("left")
            if direction != LEFT:
                Command.stop_left()
                Command.stop_right()
                Command.start_center_rudder()
                direction = LEFT
            else:
                Command.stop_center_rudder()
                Command.start_left(100)
        elif next_diff_rot < -1.0:
            # print("right")
            if direction != RIGHT:
                Command.stop_left()
                Command.stop_right()
                Command.start_center_rudder()
                direction = RIGHT
            else:
                Command.stop_center_rudder()
                Command.start_right(100)
        else:
            if direction != CENTER:
                Command.stop_left()
                Command.stop_right()
                Command.start_center_rudder()
                direction = CENTER
            else:
                Command.stop_center_rudder()


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


def check_waypoint_distance(current_waypoint, position):
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
        print("waypoint ", new_waypoint)
        if waypoint[new_waypoint][3] != -1:
            Throttle.set_max_speed(waypoint[new_waypoint][3])
            print("max speed ", waypoint[new_waypoint][3])

        if waypoint[current_waypoint][4] >= 0:
            global event_ahead_qty
            event_ahead_qty = waypoint[current_waypoint][4]

        return new_waypoint

    return current_waypoint
