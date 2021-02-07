import math

import Config


class WayPoint:
    def __init__(self):
        self.waypoint = Config.config['waypoint']
        print("waypoint quantity: " + str(len(self.waypoint)))
        self.current_waypoint = 0
        print("target waypoint: ", self.current_waypoint)
        pass

    def get_current_waypoint(self):
        return self.waypoint[self.current_waypoint]

    def check_waypoint_distance(self, position, speed):
        dist_x = position[0] - self.waypoint[self.current_waypoint][0]
        dist_z = position[1] - self.waypoint[self.current_waypoint][1]
        dist_y = position[2] - self.waypoint[self.current_waypoint][2]
        distance = math.sqrt(dist_x * dist_x + dist_y * dist_y + dist_z * dist_z)
        # print("distance: ", distance)

        proximity_distance = speed * 0.5  # distance in 0.5 seconds
        if proximity_distance < 2.0:
            proximity_distance = 2.0

        if distance < proximity_distance:
            self.current_waypoint = (self.current_waypoint + 1) % len(self.waypoint)
            print("target waypoint: ", self.current_waypoint)

            return True

        return False
