import datetime
import random

import Command


class DirectionTruckRandom:
    def __init__(self):
        self.date_direction = datetime.datetime.now()

    def run(self, rotation_diff):
        if datetime.datetime.now() > self.date_direction:
            direction = random.randrange(-100, 100)
            Command.set_TRUCK_STEER(direction)

            print("Steering wheel: ", direction)

            self.date_direction = datetime.datetime.now() + datetime.timedelta(seconds=random.random() * 10.0)

    def reset(self):
        Command.set_TRUCK_STEER(0)
        self.__init__()
