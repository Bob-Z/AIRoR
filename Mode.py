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
import SpeedNone
import SpeedTruckMax
import SpeedTruckRandom
import SpeedTruckTarget
import SpeedTruckThrottle
import TargetAvoid
import TargetNone
import TargetRandomWaypoint
import TargetWaypoint
import TargetWaypointReverse


class Mode:
    def __init__(self):
        self.thread = threading.Thread(target=push_position_button)
        self.thread.start()

        self.target = []
        if 'target' in Config.config:
            all_target = Config.config['target'].split(',')
            for t in all_target:
                if t == 'waypoint':
                    self.target.append(TargetWaypoint.TargetWaypoint())
                elif t == 'waypoint_reverse':
                    self.target.append(TargetWaypointReverse.TargetWaypointReverse())
                elif t == 'avoid':
                    self.target.append(TargetAvoid.TargetAvoid())
                elif t == 'random_waypoint':
                    self.target.append(TargetRandomWaypoint.TargetRandomWaypoint())
        else:
            self.target = [TargetNone.TargetNone()]

        self.direction = DirectionNone.DirectionNone()
        if 'direction' in Config.config:
            if Config.config['direction'] == 'truck_rotation':
                self.direction = DirectionTruckRotation.DirectionTruckRotation()
            elif Config.config['direction'] == 'truck_random':
                self.direction = DirectionTruckRandom.DirectionTruckRandom()
            elif Config.config['direction'] == 'boat_rotation':
                self.direction = DirectionBoatRotation.DirectionBoatRotation()

        self.speed = SpeedNone.SpeedNone()
        if 'speed' in Config.config:
            if Config.config['speed'] == 'truck_random':
                self.speed = SpeedTruckRandom.SpeedTruckRandom()
            elif Config.config['speed'] == 'truck_target':
                self.speed = SpeedTruckTarget.SpeedTruckTarget()
            elif Config.config['speed'] == 'truck_max':
                self.speed = SpeedTruckMax.SpeedTruckMax()
            elif Config.config['speed'] == 'truck_throttle':
                self.speed = SpeedTruckThrottle.SpeedTruckThrottle()
            elif Config.config['speed'] == 'boat_target':
                self.speed = SpeedBoatTarget.SpeedBoatTarget()

        self.height = HeightNone.HeightNone()
        if 'height' in Config.config:
            if Config.config['height'] == 'heli':
                self.height = HeightHeli.HeightHeli()

        self.reset = []
        if 'reset' in Config.config:
            all_reset = Config.config['reset'].split(',')
            for r in all_reset:
                if r == 'slow':
                    self.reset.append(ResetSlowSpeed.ResetSlowSpeed())
                if r == 'non_const':
                    self.reset.append(ResetNonConst.ResetNonConst())
                if r == 'out_of_bound':
                    self.reset.append(ResetOutOfBound.ResetOutOfBound())

        self.save = SaveNone.SaveNone()
        if 'save' in Config.config:
            if Config.config['save'] == 'avoid':
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
            for r in self.reset:
                if r.run(position, speed_ms) is True:
                    is_reset = True

            if is_reset is True:
                self.target.reset()
                self.direction.reset()
                self.speed.reset()
                self.height.reset()
                for r in self.reset:
                    r.reset()
                self.save.reset(position)


def push_position_button():
    while True:
        Command.start_COMMON_OUTPUT_POSITION()
        time.sleep(0.05)
        Command.stop_COMMON_OUTPUT_POSITION()
        time.sleep(0.05)
