import Command
import SpeedNone
import datetime
import Config


class SpeedBoatThrottle(SpeedNone.SpeedNone):
    def __init__(self):
        self.throttle_timeout = 1.5
        if 'throttle_time' in Config.config_json:
            self.throttle_timeout = Config.config_json['throttle_time']
        self.timeout_start = None

    def run(self, current_speed_ms, target_speed_ms):
        if self.timeout_start is None:
            self.timeout_start = datetime.datetime.now()

        if datetime.datetime.now() > self.timeout_start + datetime.timedelta(
                seconds=self.throttle_timeout):
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(0)
        else:
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(100)

    def reset(self):
        self.__init__()
