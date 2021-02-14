import Command

CENTER = 0
LEFT = 1
RIGHT = 2


class DirectionBoatRotation:
    def __init__(self):
        self.direction = CENTER
        pass

    def run(self, rotation_diff):
        if rotation_diff > 1.0:
            # print("left")
            if self.direction != LEFT:
                Command.BOAT_STEER_RIGHT(0)
                Command.BOAT_STEER_LEFT(0)
                Command.start_BOAT_CENTER_RUDDER()
                self.direction = LEFT
            else:
                Command.stop_BOAT_CENTER_RUDDER()
                Command.BOAT_STEER_LEFT(100)
        elif rotation_diff < -1.0:
            # print("right")
            if self.direction != RIGHT:
                Command.BOAT_STEER_RIGHT(0)
                Command.BOAT_STEER_LEFT(0)
                Command.start_BOAT_CENTER_RUDDER()
                self.direction = RIGHT
            else:
                Command.stop_BOAT_CENTER_RUDDER()
                Command.BOAT_STEER_RIGHT(100)
        else:
            if self.direction != CENTER:
                Command.BOAT_STEER_RIGHT(0)
                Command.BOAT_STEER_LEFT(0)
                Command.start_BOAT_CENTER_RUDDER()
                self.direction = CENTER
            else:
                Command.stop_BOAT_CENTER_RUDDER()

    def reset(self):
        self.__init__()
        Command.BOAT_STEER_LEFT(0)
        Command.BOAT_STEER_RIGHT(0)
        Command.stop_BOAT_CENTER_RUDDER()
