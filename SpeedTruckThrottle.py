import time

import Command
import Config
import SpeedNone
import datetime


class SpeedTruckThrottle(SpeedNone.SpeedNone):
    def __init__(self):
        if 'throttle_percent' in Config.config_json:
            self.throttle_percent = Config.config_json['throttle_percent']
        else:
            self.throttle_percent = 50.0

        self.start_time = datetime.datetime.now()

        self.is_autoshift_down = False

        print("[Speed truck throttle] ", self.throttle_percent, "%")

    def run(self, speed_ms, target_speed_ms):
        if datetime.datetime.now() > self.start_time + datetime.timedelta(seconds=0.8):
            Command.TRUCK_ACCELERATE(self.throttle_percent)

        else:  # Initial full throttle to start engine
            Command.TRUCK_ACCELERATE(100.0)

        if self.is_autoshift_down is True:
            Command.stop_AUTOSHIFT_DOWN()
            self.is_autoshift_down = False
        else:
            Command.start_AUTOSHIFT_DOWN()
            self.is_autoshift_down = True

    def reset(self):
        Command.TRUCK_BRAKE(0)
        Command.TRUCK_ACCELERATE(0)
        self.__init__()
