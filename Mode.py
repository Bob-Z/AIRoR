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
import ResetNone
import ResetSlowSpeed
import SaveMap
import SaveNone
import SpeedBoatTarget
import SpeedNone
import SpeedTruckMax
import SpeedTruckRandom
import SpeedTruckTarget
import SpeedTruckThrottle
import TargetNone
import TargetWaypoint


class Mode:
    def __init__(self):
        self.thread = threading.Thread(target=push_position_button)
        self.thread.start()

        self.target = TargetNone.TargetNone()
        if 'target' in Config.config:
            if Config.config['target'] == 'waypoint':
                self.target = TargetWaypoint.TargetWaypoint()

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

        self.reset = ResetNone.ResetNone()
        if 'reset' in Config.config:
            if Config.config['reset'] == 'slow':
                self.reset = ResetSlowSpeed.ResetSlowSpeed()
            if Config.config['reset'] == 'non_const':
                self.reset = ResetNonConst.ResetNonConst()

        self.save = SaveNone.SaveNone()
        if 'save' in Config.config:
            if Config.config['save'] == 'map':
                self.save = SaveMap.SaveMap()

    def run(self):
        while True:
            Event.wait()

            position = Input.get_position()
            rotation = Input.get_rotation()
            speed_ms = Input.get_speed_norm()

            rot_diff, target_speed_ms, go_up = self.target.run(position, rotation, speed_ms)

            self.direction.run(rot_diff)

            self.speed.run(speed_ms, target_speed_ms)

            self.height.run(go_up)

            if self.reset.run(speed_ms) is True:
                self.target.reset()
                self.direction.reset()
                self.speed.reset()
                self.height.reset()
                self.reset.reset()
                self.save.reset(position)


def push_position_button():
    while True:
        Command.start_COMMON_OUTPUT_POSITION()
        time.sleep(0.05)
        Command.stop_COMMON_OUTPUT_POSITION()
        time.sleep(0.05)
