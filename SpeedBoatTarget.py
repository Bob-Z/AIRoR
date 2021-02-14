import Command


class SpeedBoatTarget:
    def __init__(self):
        pass

    def run(self, current_speed_ms, target_speed_ms):
        if current_speed_ms < target_speed_ms - target_speed_ms * 0.05:
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(100)
        else:
            if current_speed_ms > target_speed_ms:
                Command.TRUCK_BRAKE(100)
                Command.TRUCK_ACCELERATE(0)
            else:
                Command.TRUCK_BRAKE(0)
                Command.TRUCK_ACCELERATE(0)

    def reset(self):
        self.__init__()
        Command.TRUCK_BRAKE(0)
        Command.TRUCK_ACCELERATE(0)
