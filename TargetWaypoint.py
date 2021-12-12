import math

import Config
import Math
import TargetNone


class TargetWaypoint(TargetNone.TargetNone):
    def __init__(self, reverse=False):
        self.waypoint = Config.config['waypoint']
        print("[Target waypoint] " + str(len(self.waypoint)) + " waypoints")

        if 'proximity_timeout' in Config.config:
            self.proximity_timeout = Config.config['proximity_timeout']
        else:
            self.proximity_timeout = 0.5
        print("[Target waypoint] proximity timeout = " + str(self.proximity_timeout))

        self.event_ahead_qty = 1

        self.current_waypoint = 0
        self.prev_rotation = [0.0, 0.0, 0.0]

        self.target_speed_ms = self.waypoint[self.current_waypoint][3] * 1000 / 3600
        self.rot_diff = 0.0

        self.previous_height = 0.0
        self.height_event_ahead_qty = 10
        self.go_up = False

        self.reverse = reverse

    def reset(self):
        self.event_ahead_qty = 1

        self.current_waypoint = 0
        self.prev_rotation = [0.0, 0.0, 0.0]

        self.target_speed_ms = self.waypoint[self.current_waypoint][3] * 1000 / 3600
        self.rot_diff = 0.0

        self.previous_height = 0.0
        self.height_event_ahead_qty = 10
        self.go_up = False

        print("[Target waypoint] reset")

    def run(self, position, rotation, speed_ms, rot_diff, target_speed_ms, go_up):
        self.check_waypoint_distance(position, speed_ms)

        self.check_rotation(position, rotation)

        self.check_height(position)

        return self.rot_diff, self.target_speed_ms, self.go_up

    def check_waypoint_distance(self, position, speed_ms):
        proximity_distance = speed_ms * self.proximity_timeout
        if proximity_distance < 2.0:
            proximity_distance = 2.0

        waypoint_changed = False

        while True:
            dist_x = position[0] - self.waypoint[self.current_waypoint][0]
            dist_z = position[1] - self.waypoint[self.current_waypoint][1]
            dist_y = position[2] - self.waypoint[self.current_waypoint][2]
            distance = math.sqrt(dist_x * dist_x + dist_y * dist_y + dist_z * dist_z)

            if distance > proximity_distance:
                break

            if self.reverse is False:
                new_waypoint = (self.current_waypoint + 1) % len(self.waypoint)
            else:
                new_waypoint = (self.current_waypoint - 1);
                if new_waypoint < 0:
                    new_waypoint = len(self.waypoint) - 1

            if self.waypoint[new_waypoint][3] != -1:
                self.target_speed_ms = self.waypoint[new_waypoint][3] * 1000 / 3600

            if self.waypoint[self.current_waypoint][4] >= 0:
                self.event_ahead_qty = self.waypoint[self.current_waypoint][4]

            self.current_waypoint = new_waypoint

            waypoint_changed = True

        if waypoint_changed is True:
            print("[Target Waypoint] new waypoint ", new_waypoint, "speed kmh = ", self.target_speed_ms / 1000 * 3600, ", event ahead = ",
                  self.event_ahead_qty)

    def check_rotation(self, position, rotation):
        waypoint_angle = Math.calc_angle([position[0], position[2] + 1.0], [position[0], position[2]],
                                         [self.waypoint[self.current_waypoint][0],
                                          self.waypoint[self.current_waypoint][2]])

        if waypoint_angle > 0:
            target_angle = waypoint_angle - 180.0
        else:
            target_angle = waypoint_angle + 180.0
        # print('target_angle: ', target_angle)
        # print('rotation:', rotation)

        # diff_rot = rotation[1] - target_angle
        # print('rotation[1] - target_angle:', diff_rot)

        rotation_since_previous_event = self.prev_rotation[1] - rotation[1]

        next_diff_rot = rotation[1] - (self.event_ahead_qty * rotation_since_previous_event) - target_angle

        self.prev_rotation = rotation

        if next_diff_rot > 180.0:
            next_diff_rot = next_diff_rot - 360.0
        if next_diff_rot < -180.0:
            next_diff_rot = 360.0 + next_diff_rot
        # print("diff_rot = ", diff_rot)

        self.rot_diff = next_diff_rot

    def check_height(self, position):
        height_since_previous_event = self.previous_height - position[1]
        next_height = position[1] - (self.event_ahead_qty * height_since_previous_event)

        self.previous_height = position[1]

        if next_height < self.waypoint[self.current_waypoint][1]:
            self.go_up = True
        else:
            self.go_up = False
