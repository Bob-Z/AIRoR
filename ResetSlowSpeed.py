import datetime
import time

import Command
import ResetNone


class ResetSlowSpeed(ResetNone.ResetNone):
    def __init__(self):
        self.slow_speed = False
        self.previous_slow_speed = False
        self.slow_speed_timestamp = datetime.datetime.now()
        self.first_run = True

    def run(self, position, current_speed_ms):
        if self.first_run is True:
            self.slow_speed_timestamp = datetime.datetime.now()

        if current_speed_ms < 0.05:
            if self.slow_speed is False:
                print("[Reset slow speed] Slow speed detected")
            self.slow_speed = True
        else:
            if self.slow_speed is True:
                print("[Reset slow speed] No slow speed anymore")
            self.slow_speed = False

        if self.previous_slow_speed is False and self.slow_speed is True:
            self.slow_speed_timestamp = datetime.datetime.now()

        self.previous_slow_speed = self.slow_speed

        if self.slow_speed is True and datetime.datetime.now() > self.slow_speed_timestamp + datetime.timedelta(
                seconds=4):
            print("[Reset slow speed] Reset vehicle")
            Command.start_COMMON_RESET_TRUCK()
            time.sleep(0.1)
            Command.stop_COMMON_RESET_TRUCK()

            return True, position

        return False, None
