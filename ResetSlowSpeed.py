import datetime
import time

import Command
import Input


class ResetSlowSpeed:
    def __init__(self):
        self.slow_speed = False
        self.previous_slow_speed = False
        self.slow_speed_timestamp = datetime.datetime.now()

    def run(self, current_speed_ms):
        if current_speed_ms < 0.05:
            if self.slow_speed is False:
                print("Slow speed detected")
            self.slow_speed = True
        else:
            if self.slow_speed is True:
                print("Slow speed reset")
            self.slow_speed = False

        if self.previous_slow_speed is False and self.slow_speed is True:
            self.slow_speed_timestamp = datetime.datetime.now()

        self.previous_slow_speed = self.slow_speed

        if self.slow_speed is True and datetime.datetime.now() > self.slow_speed_timestamp + datetime.timedelta(
                seconds=4):
            print("Reset vehicle")
            Command.start_COMMON_RESET_TRUCK()
            time.sleep(0.1)
            Command.stop_COMMON_RESET_TRUCK()
            self.slow_speed = False
            self.previous_slow_speed = False

            return True

        return False
