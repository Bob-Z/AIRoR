import Command
import DirectionNone


class DirectionTruckRotation(DirectionNone.DirectionNone):
    def __init__(self):
        self.previous_force = 0
        self.smoothness = 10
        pass

    def run(self, rotation_diff):
        # wheel_force = max(5, abs(diff_rot) * 1.5)
        #wheel_force = 10 + abs(rotation_diff)
        wheel_force = rotation_diff
        # print("wheel force: ", wheel_force)

        diff_force = wheel_force - self.previous_force

        diff_force = min(diff_force, self.smoothness)
        diff_force = max(diff_force, -self.smoothness)

        self.previous_force = self.previous_force + diff_force

        new_wheel_force = abs(self.previous_force)

        if self.previous_force > 10.0:
            # print("left")
            Command.TRUCK_STEER_LEFT(new_wheel_force + 10)
        elif self.previous_force < -10.0:
            # print("right")
            Command.TRUCK_STEER_RIGHT(new_wheel_force + 10)
        else:
            Command.TRUCK_STEER_RIGHT(0)

    def reset(self):
        self.__init__()
        Command.TRUCK_STEER_LEFT(0)
        Command.TRUCK_STEER_RIGHT(0)
        self.previous_force = 0
