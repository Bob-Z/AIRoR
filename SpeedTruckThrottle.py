import Command
import Config
import SpeedNone
import datetime


class SpeedTruckThrottle(SpeedNone.SpeedNone):
    def __init__(self):
        if 'throttle_percent' in Config.config:
            self.throttle_percent = Config.config['throttle_percent']
        else:
            self.throttle_percent = 50.0

        self.start_time = datetime.datetime.now()

        print("[Speed truck throttle] ", self.throttle_percent, "%")

    def run(self, speed_ms, target_speed_ms):
        if datetime.datetime.now() > self.start_time + datetime.timedelta(seconds=0.8):
            Command.TRUCK_ACCELERATE(self.throttle_percent)
        else:  # Initial full throttle to start engine
            Command.TRUCK_ACCELERATE(100.0)
