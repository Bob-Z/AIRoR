import Command
import SpeedNone
import datetime
import Config


class SpeedBoatThrottle(SpeedNone.SpeedNone):
    def __init__(self):
        self.timeout_start = datetime.datetime.now()
        self.throttle_timeout = 1.5
        if 'throttle_time' in Config.config:
            self.throttle_timeout = Config.config['throttle_time']

    def run(self, current_speed_ms, target_speed_ms):
        if datetime.datetime.now() > self.timeout_start + datetime.timedelta(
            seconds=self.throttle_timeout):
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(0)
        else:
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(100)

    def reset(self):
        self.__init__()
        self.timeout_start = datetime.datetime.now()
        Command.TRUCK_BRAKE(0)
        Command.TRUCK_ACCELERATE(0)

