import math

import TargetNone
import random


class TargetRandomAngle(TargetNone.TargetNone):
    def __init__(self):
        self.angle = random.random() * 360.0
        print("[Target random angle] angle", self.angle)

    def reset(self):
        self.angle = random.random() * 360.0
        print("[Target random angle] angle", self.angle)

    def run(self, position, rotation, speed_ms, rot_diff, target_speed_ms, go_up):
        rot_diff = rotation[1] - self.angle
        if rot_diff > 180.0:
            rot_diff = rot_diff - 360.0
        if rot_diff < -180.0:
            rot_diff = 360.0 + rot_diff
        return rot_diff, 0.0, False
