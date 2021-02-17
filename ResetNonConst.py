import time

import Command


class ResetNonConst:
    def __init__(self):
        self.is_move_detected = False
        self.is_target_speed_detected = False
        self.is_constant = False
        self.target_speed = 0.0
        self.previous_speed = 0.0
        self.move_step_qty = 0
        self.const_step_qty = 0
        self.non_target_step_qty = 0

    def run(self, current_speed_ms):
        if self.is_move_detected is False:
            if current_speed_ms > 0.1:
                self.move_step_qty += 1
        else:
            if self.is_target_speed_detected is False:
                if self.previous_speed * 0.98 < current_speed_ms < self.previous_speed * 1.02:
                    if self.is_constant is False:
                        print("Constant speed")
                    self.is_constant = True
                    self.const_step_qty += 1
                self.previous_speed = current_speed_ms
            else:
                if current_speed_ms * 0.90 < self.target_speed < current_speed_ms * 1.10:
                    self.target_speed = current_speed_ms
                    self.non_target_step_qty = 0
                else:
                    print("Target speed diff = ", self.target_speed - current_speed_ms)
                    self.non_target_step_qty += 1

        if self.is_move_detected is False:
            if self.move_step_qty > 5:
                self.is_move_detected = True
                print("Move detected")
        else:
            if self.is_target_speed_detected is False:
                if self.const_step_qty > 10:
                    self.is_target_speed_detected = True
                    self.target_speed = current_speed_ms
                    print("Target speed = ", self.target_speed)
            else:
                if self.non_target_step_qty > 10:
                    print("NON target speed detected - reset Vehicle")
                    Command.start_COMMON_RESET_TRUCK()
                    time.sleep(0.1)
                    Command.stop_COMMON_RESET_TRUCK()

                    return True

        return False

    def reset(self):
        self.__init__()
