import time

import Command
import Config
import ResetNone


class ResetOutOfBound(ResetNone.ResetNone):
    def __init__(self):
        # This is "simple" terrain bounds
        self.bound = [487.0, 487.0, 537.0, 537.0]

        if 'bound' in Config.config:
            self.bound = Config.config['bound']

    def run(self, position, current_speed_ms):
        minX = min(self.bound[0], self.bound[2])
        maxX = max(self.bound[0], self.bound[2])
        minY = min(self.bound[1], self.bound[3])
        maxY = max(self.bound[1], self.bound[3])

        if position[0] < minX or position[0] > maxX or position[2] < minY or position[2] > maxY:
            print("Out of bound - Reset vehicle")
            Command.start_COMMON_RESET_TRUCK()
            time.sleep(0.1)
            Command.stop_COMMON_RESET_TRUCK()

            return True

        return False
