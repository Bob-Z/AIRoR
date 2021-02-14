import datetime
import random

import SpeedTruckMax


class SpeedTruckRandom:
    def __init__(self):
        self.date_traction = datetime.datetime.now()
        self.go_forward = False
        self.random_speed_ms = 0.0
        self.traction = SpeedTruckMax.SpeedTruckMax()

    def run(self, speed_ms, target_speed_ms):
        if datetime.datetime.now() > self.date_traction:
            rand = random.randrange(3)
            if rand == 0 or rand == 1:
                if self.go_forward is False:
                    print("Go forward")
                self.traction.forward()
                self.go_forward = True
            if rand == 2:
                print("Go backward")
                self.traction.backward()
                self.go_forward = False

            self.date_traction = datetime.datetime.now() + datetime.timedelta(seconds=random.random() * 10.0)

            self.random_speed_ms = random.random() * 30.0
            print("Random speed: ", self.random_speed_ms)

        self.traction.run(speed_ms, self.random_speed_ms)

    def reset(self):
        self.__init__()
