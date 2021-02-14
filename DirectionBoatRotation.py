import Command


class DirectionBoatRotation:
    def __init__(self):
        pass

    def run(self, rotation_diff):
        # wheel_force = max(5, abs(diff_rot) * 1.5)
        wheel_force = 10 + abs(rotation_diff)
        # print("wheel force: ", wheel_force)

        if rotation_diff > 0.0:
            # print("left")
            Command.BOAT_STEER_LEFT(wheel_force)
        else:
            # print("right")
            Command.BOAT_STEER_RIGHT(wheel_force)

    def reset(self):
        Command.BOAT_STEER_LEFT(0)
        Command.BOAT_STEER_RIGHT(0)
