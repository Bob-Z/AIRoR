import Command
import SpeedNone


class SpeedTruckMax(SpeedNone.SpeedNone):
    def __init__(self):
        pass

    def run(self, current_speed_ms, target_speed_ms):
        Command.TRUCK_ACCELERATE(100)

    def reset(self):
        Command.TRUCK_ACCELERATE(0)
        self.__init__()
