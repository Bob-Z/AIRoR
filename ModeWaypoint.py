import math

import numpy as np

import Command
import Event
import Input
import Traction

# waypoint = [[512.0, 0.0, 512.0], [412.0, 0.0, 512.0]]

waypoint = [[882.132996, 0.120613, 1324.317139, 250],
            [671.969, 0.628959, 1327.45, 80],
            [630.046, 0.495165, 1316.58, 72],
            [600.246, 0.493378, 1287.67, None],
            [575.756, 0.495862, 1230.29, None],
            [576.293, 0.49587, 1135.25, 120],
            [573.385, 0.492764, 1068.6, 90],
            [566.941, 0.498048, 1040.65, 70],
            [547.127, 0.495708, 1008.84, None],
            [522.018, 0.491687, 991.464, None],
            [450.689, 0.495061, 949.769, 110],  # 10
            [362.713, 0.495408, 896.579, None],
            [326.897, 0.200916, 857.079, 72],
            [315.591, 0.200907, 819.597, None],
            [323.362, 0.200916, 764.728, None],
            [343.011, 0.201, 737.128, None],
            [374.705, 0.201, 724.259, None],
            [410.43, 0.494596, 722.019, 97],
            [460.298, 0.493186, 720.877, 108],
            [524.83, 0.494454, 721.16, None],
            [589.659, 0.493172, 736.214, 90],  # 20
            [672.196, 0.494605, 762.288, None],
            [767.108, 0.494509, 761.482, 92],
            [799.829, 0.494724, 758.56, None],
            [882.275, 0.490555, 724.467, None],
            [969.205, 0.494669, 677.169, 95],
            [1040.43, 0.491678, 662.585, None],
            [1108.12, 0.494391, 664.198, None],
            [1306.22, 0.489011, 661.913, 208],
            [1389.63, 0.496277, 664.109, 99],
            [1417.24, 0.496141, 673.255, 50],  # 30
            [1451.29, 0.50119, 698.982, None],
            [1463.32, 0.200763, 728.697, None],
            [1456.7, 0.494567, 779.487, 103, None],
            [1441.16, 0.493304, 837.027, 204],
            [1428.65, 0.494075, 901.961, None],
            [1415.7, 0.497855, 975.794, None],
            [1415.29, 0.498023, 1051.97, 107],
            [1449.38, 0.490844, 1172.53, None],
            [1483.74, 0.495477, 1278.44, None],
            [1493.61, 0.200977, 1308.01, 50],  # 40
            [1492.99, 0.200987, 1330.46, None],
            [1481.7, 0.200986, 1345.72, None],
            [1461.23, 0.201001, 1351.46, None],
            [1441.87, 0.200992, 1343.01, 104],
            [1410.13, 0.200992, 1328.48, 220],
            [892.132996, 0.120613, 1324.317139, None]]


def init():
    pass


def run():
    Traction.forward()

    current_waypoint = 0
    if waypoint[current_waypoint][3] is not None:
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
        if waypoint[new_waypoint][3] is not None:
            Traction.set_max_speed(waypoint[new_waypoint][3])
        print("max speed ", waypoint[new_waypoint][3])

        return new_waypoint

    return current_waypoint
