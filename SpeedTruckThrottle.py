import Config
import Command


class SpeedTruckThrottle:
    def __init__(self):
        if 'throttle_percent' in Config.config:
            self.throttle_percent = Config.config['throttle_percent']
        else:
            self.throttle_percent = 50.0

        print("Speed truck throttle : ", self.throttle_percent)

    def run(self, speed_ms, target_speed_ms):
        Command.TRUCK_ACCELERATE(self.throttle_percent)

    def reset(self):
        self.__init__()
