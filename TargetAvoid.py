import math
import datetime

import Config
import Math
import TargetNone

class TargetAvoid(TargetNone.TargetNone):
    def __init__(self):
        self.avoid_coordinate = Config.config['avoid']
        print("[Target avoid] " + str(len(self.avoid_coordinate)) + " avoidance coordinates")

        self.target_speed_ms = 0.0
        self.rot_diff = 0.0

        self.go_up = False

        self.timestamp = datetime.datetime.now()

        self.obstacle_ahead = False

        self.travel_duration_min_s = 3.0
        self.travel_duration_max_s = 8.0
        self.init_travel_duration_s = self.travel_duration_min_s
        self.travel_duration_s = self.init_travel_duration_s
        print("[Target avoid] travel_duration =", self.travel_duration_s)

        self.is_give_up = False

        self.previous_angle_sign = 1

    def reset(self):
        self.avoid_coordinate = Config.config['avoid']
        print("[Target avoid] " + str(len(self.avoid_coordinate)) + " avoidance coordinates")

        self.target_speed_ms = 0.0
        self.rot_diff = 0.0

        self.go_up = False

        self.timestamp = datetime.datetime.now()

        self.obstacle_ahead = False

        self.init_travel_duration_s = self.init_travel_duration_s + 0.5
        if self.init_travel_duration_s > self.travel_duration_max_s:
            self.init_travel_duration_s = self.travel_duration_min_s

        self.travel_duration_s = self.init_travel_duration_s
        print("[Target avoid] travel_duration = ", self.travel_duration_s, "s")

        self.is_give_up = False

        self.previous_angle_sign = 1

    def run(self, position, rotation, speed_ms, rot_diff, target_speed_ms, go_up):
        current_timestamp = datetime.datetime.now()

        if current_timestamp - self.timestamp > datetime.timedelta(seconds=0.0):  # FIXME: hard coded value
            # Not sure why I have to make this but, RoRBot and trucks have not the same orientation
            rotation[1] = rotation[1] + 90

            rotation[1] = rotation[1] + rot_diff # rotation with regards results of previous "target" configuration

            self.find_avoidance_parameters(position, rotation)

            self.timestamp = current_timestamp

            return self.rot_diff + rot_diff, self.target_speed_ms, self.go_up
        else:
            return rot_diff, self.target_speed_ms, self.go_up

    def find_avoidance_parameters(self, position, rotation):
        speed_ms = 2.8  # FIXME hard coded value

        travel_distance_m = speed_ms * self.travel_duration_s
        current_rotation = rotation[1]

        if self.is_obstacle_ahead(position, current_rotation, travel_distance_m) is True:
            if self.obstacle_ahead is True:
                print("[TargetAvoid] No more obstacle ahead within",travel_distance_m,"m,",self.travel_duration_s,"s")
                self.obstacle_ahead = False
            self.rot_diff = 0
            self.target_speed_ms = speed_ms
            self.is_give_up = False
            return

        while self.travel_duration_s > self.travel_duration_min_s - 0.1:
            for rot_diff in range(5, 175, 5):
                # print("trying rotation", current_rotation + rot_diff)
                if self.is_obstacle_ahead(position, current_rotation + rot_diff, travel_distance_m) is True:
                    # print("rotation", -rot_diff, "OK")
                    self.rot_diff = -rot_diff
                    self.target_speed_ms = speed_ms
                    self.is_give_up = False
                    self.previous_angle_sign = -1
                    return
                # print("trying rotation", current_rotation - rot_diff)
                if self.is_obstacle_ahead(position, current_rotation - rot_diff, travel_distance_m) is True:
                    # print("rotation", rot_diff, "OK")
                    self.rot_diff = rot_diff
                    self.target_speed_ms = speed_ms
                    self.is_give_up = False
                    self.previous_angle_sign = 1
                    return

            print("[TargetAvoid] dead end within", travel_distance_m,"m,",self.travel_duration_s,"s")
            self.travel_duration_s = self.travel_duration_s / 2.0
            travel_distance_m = speed_ms * self.travel_duration_s
            print("[TargetAvoid] Lower travel distance to", travel_distance_m,"m,",self.travel_duration_s,"s")

        self.rot_diff = self.previous_angle_sign * 180
        if self.is_give_up is False:
            print("[TargetAvoid] give-up, trying", self.rot_diff)
        self.is_give_up = True

    def is_obstacle_ahead(self, position, rotation, distance_m):
        # print("Checking rotation", rotation)

        # Build rectangle and check it avoids everything
        rect = [
            [
                0,
                -2.0  # FIX ME hard coded value - 2 meters right
            ],
            [
                0,
                2.0  # FIX ME hard coded value - 2 meters left
            ],
            [
                -distance_m,  # FIX ME hard coded value - 50 meters ahead
                2.0  # FIX ME hard coded value - 2 meters left
            ],
            [
                -distance_m,  # FIX ME hard coded value - 50 meters ahead
                -2.0  # FIX ME hard coded value - 2 meters right
            ]
        ]

        # print("rect", rect)

        angle_rad = math.radians(rotation)
        s = math.sin(angle_rad)
        c = math.cos(angle_rad)

        rotated_rect = [
            [
                c * rect[0][0] - s * rect[0][1],
                s * rect[0][0] + c * rect[0][1],
            ],
            [
                c * rect[1][0] - s * rect[1][1],
                s * rect[1][0] + c * rect[1][1],
            ],
            [
                c * rect[2][0] - s * rect[2][1],
                s * rect[2][0] + c * rect[2][1],
            ],
            [
                c * rect[3][0] - s * rect[3][1],
                s * rect[3][0] + c * rect[3][1],
            ]
        ]

        # print("rotated_rect", rotated_rect)

        final_rect = [
            [
                rotated_rect[0][0] + position[0],
                rotated_rect[0][1] + position[2]
            ],
            [
                rotated_rect[1][0] + position[0],
                rotated_rect[1][1] + position[2]
            ],
            [
                rotated_rect[2][0] + position[0],
                rotated_rect[2][1] + position[2]
            ],
            [
                rotated_rect[3][0] + position[0],
                rotated_rect[3][1] + position[2]
            ]
        ]

        # print("final rect", final_rect)

        for coord in self.avoid_coordinate:
            test_point = [coord[0], coord[2]]
            if Math.point_in_rectangle(test_point, final_rect) is True:
                if self.obstacle_ahead is False:
                    print("[TargetAvoid] Obstacle within",distance_m,"m")
                    self.obstacle_ahead = True
                return False

        # print("distance=", distance_m, "angle=", angle, "free")
        return True
