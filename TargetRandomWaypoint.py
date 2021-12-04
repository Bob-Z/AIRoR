import math

import Config
import Math
import TargetNone
import random
import datetime


class TargetRandomWaypoint(TargetNone.TargetNone):
    def __init__(self):
        # self.waypoint = Config.config['waypoint']
        print("Target mode random waypoint")

        if 'proximity_distance' in Config.config:
            self.proximity_distance = Config.config['proximity_distance']
        else:
            self.proximity_distance = 10
        print("[Target random waypoint] proximity distance = " + str(self.proximity_distance))

        self.bound = [0.0, 0.0, 5000.0, 5000.0]
        if 'bound' in Config.config:
            self.bound = Config.config['bound']
        print("[Target random waypoint] bound =", self.bound)

        self.rand_x = self.get_random_x()
        self.rand_y = self.get_random_y()
        print("[Target random waypoint] new way point", self.rand_x, self.rand_y)

        self.rot_diff = 0.0

        self.new_waypoint_timeout = 15*60 # 15 minutes
        self.timeout_start = datetime.datetime.now()

    def reset(self):
        self.rand_x = self.get_random_x()
        self.rand_y = self.get_random_y()
        print("[Target random waypoint] reset - new way point", self.rand_x, self.rand_y)

    def run(self, position, rotation, speed_ms, rot_diff, target_speed_ms, go_up):
        self.check_timeout()

        self.check_waypoint_distance(position, speed_ms)

        self.calc_rotation(position, rotation)

        # return self.rot_diff, self.target_speed_ms, self.go_up
        return self.rot_diff, 0.0, False

    def check_waypoint_distance(self, position, speed_ms):
        dist_x = position[0] - self.rand_x
        dist_y = position[2] - self.rand_y
        distance = math.sqrt(dist_x * dist_x + dist_y * dist_y)
        # print("distance: ", distance)

        if distance < self.proximity_distance:
            self.rand_x = self.get_random_x()
            self.rand_y = self.get_random_y()
            print("[Target random waypoint] waypoint reached - new way point", self.rand_x, self.rand_y)

    def check_timeout(self):
        if datetime.datetime.now() > self.timeout_start + datetime.timedelta(
                seconds=self.new_waypoint_timeout):
            self.rand_x = self.get_random_x()
            self.rand_y = self.get_random_y()

            self.timeout_start = datetime.datetime.now()
            print("[Target random waypoint] timeout - new way point", self.rand_x, self.rand_y)


    def calc_rotation(self, position, rotation):
        waypoint_angle = Math.calc_angle([position[0], position[2] - 1.0], [position[0], position[2]],
                                         [self.rand_x,
                                          self.rand_y])

        self.rot_diff = rotation[1] - waypoint_angle

        if self.rot_diff > 180.0:
            self.rot_diff = self.rot_diff - 360.0
        if self.rot_diff < -180.0:
            self.rot_diff = 360.0 + self.rot_diff

    def get_random_x(self):
        width = self.bound[2] - self.bound[0]
        return self.bound[0] + random.random() * width

    def get_random_y(self):
        height = self.bound[3] - self.bound[1]
        return self.bound[1] + random.random() * height
