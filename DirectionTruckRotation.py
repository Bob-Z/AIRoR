import Command
import DirectionNone


class DirectionTruckRotation(DirectionNone.DirectionNone):
    def __init__(self):
        pass

    def run(self, rotation_diff):
        # wheel_force = max(5, abs(diff_rot) * 1.5)
        wheel_force = 10 + abs(rotation_diff)
        # print("wheel force: ", wheel_force)

        if rotation_diff > 0.0:
            # print("left")
            Command.TRUCK_STEER_LEFT(wheel_force)
        else:
            # print("right")
            Command.TRUCK_STEER_RIGHT(wheel_force)

    def reset(self):
        self.__init__()
        Command.TRUCK_STEER_LEFT(0)
        Command.TRUCK_STEER_RIGHT(0)
