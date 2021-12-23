import threading
import time

import Command
import Config
import DirectionBoatRotation
import DirectionNone
import DirectionTruckRandom
import DirectionTruckRotation
import Event
import HeightHeli
import HeightNone
import Input
import ResetNonConst
import ResetOutOfBound
import ResetSlowSpeed
import SaveAvoid
import SaveNone
import SpeedBoatTarget
import SpeedBoatThrottle
import SpeedNone
import SpeedTruckMax
import SpeedTruckRandom
import SpeedTruckTarget
import SpeedTruckThrottle
import TargetAvoid
import TargetNone
import TargetRandomAngle
import TargetRandomWaypoint
import TargetWaypoint
import TargetWaypointReverse


class Mode:
    def __init__(self):
        self.thread = threading.Thread(target=push_position_button)
        self.thread.start()

        self.target = []
        if 'target' in Config.config_json:
            all_target = Config.config_json['target'].split(',')
            for t in all_target:
                if t == 'waypoint':
                    self.target.append(TargetWaypoint.TargetWaypoint())
                elif t == 'waypoint_reverse':
                    self.target.append(TargetWaypointReverse.TargetWaypointReverse())
                elif t == 'avoid':
                    self.target.append(TargetAvoid.TargetAvoid())
                elif t == 'random_waypoint':
                    self.target.append(TargetRandomWaypoint.TargetRandomWaypoint())
                elif t == 'random_angle':
                    self.target.append(TargetRandomAngle.TargetRandomAngle())
        else:
            self.target = [TargetNone.TargetNone()]

        self.direction = DirectionNone.DirectionNone()
        if 'direction' in Config.config_json:
            if Config.config_json['direction'] == 'truck_rotation':
                self.direction = DirectionTruckRotation.DirectionTruckRotation()
            elif Config.config_json['direction'] == 'truck_random':
                self.direction = DirectionTruckRandom.DirectionTruckRandom()
            elif Config.config_json['direction'] == 'boat_rotation':
                self.direction = DirectionBoatRotation.DirectionBoatRotation()

        self.speed = SpeedNone.SpeedNone()
        if 'speed' in Config.config_json:
            if Config.config_json['speed'] == 'truck_random':
                self.speed = SpeedTruckRandom.SpeedTruckRandom()
            elif Config.config_json['speed'] == 'truck_target':
                self.speed = SpeedTruckTarget.SpeedTruckTarget()
            elif Config.config_json['speed'] == 'truck_max':
                self.speed = SpeedTruckMax.SpeedTruckMax()
            elif Config.config_json['speed'] == 'truck_throttle':
                self.speed = SpeedTruckThrottle.SpeedTruckThrottle()
            elif Config.config_json['speed'] == 'boat_target':
                self.speed = SpeedBoatTarget.SpeedBoatTarget()
            elif Config.config_json['speed'] == 'boat_throttle':
                self.speed = SpeedBoatThrottle.SpeedBoatThrottle()

        self.height = HeightNone.HeightNone()
        if 'height' in Config.config_json:
            if Config.config_json['height'] == 'heli':
                self.height = HeightHeli.HeightHeli()

        self.reset = []
        if 'reset' in Config.config_json:
            all_reset = Config.config_json['reset'].split(',')
            for r in all_reset:
                if r == 'slow':
                    self.reset.append(ResetSlowSpeed.ResetSlowSpeed())
                if r == 'non_const':
                    self.reset.append(ResetNonConst.ResetNonConst())
                if r == 'out_of_bound':
                    self.reset.append(ResetOutOfBound.ResetOutOfBound())

        self.save = SaveNone.SaveNone()
        if 'save' in Config.config_json:
            if Config.config_json['save'] == 'avoid':
                self.save = SaveAvoid.SaveAvoid()

    def run(self):
        while True:
            Event.wait()

            position = Input.get_position()
            rotation = Input.get_rotation()
            speed_ms = Input.get_speed_norm()

            rot_diff = 0.0
            target_speed_ms = 0.0
            go_up = False
            for t in self.target:
                rot_diff, target_speed_ms, go_up = t.run(position, rotation, speed_ms, rot_diff, target_speed_ms, go_up)

            self.direction.run(rot_diff)

            self.speed.run(speed_ms, target_speed_ms)

            self.height.run(go_up)

            is_reset = False
            reset_position = None
            for r in self.reset:
                is_reset, reset_position = r.run(position, speed_ms)
                if is_reset is True:
                    break

            if is_reset is True:
                for t in self.target:
                    t.reset()
                self.direction.reset()
                self.speed.reset()
                self.height.reset()
                for r in self.reset:
                    r.reset()
                self.save.reset(reset_position)

                Input.reset()


def push_position_button():
    while True:
        Command.start_COMMON_OUTPUT_POSITION()
        time.sleep(0.05)
        Command.stop_COMMON_OUTPUT_POSITION()
        time.sleep(0.05)
