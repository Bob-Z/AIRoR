import Command
import Config
import SpeedNone


class SpeedTruckTarget(SpeedNone.SpeedNone):
    def __init__(self):
        self.current_target_speed_ms = 0.0

        self.go_forward = True
        #self.traction_force = 100

        self.num_previous_speed = 4
        self.previous_speed_array = []

        self.max_traction = 100
        if 'max_traction' in Config.config_json:
            self.max_traction = Config.config_json['max_traction']

        self.current_traction = self.max_traction

        self.is_accelerating = False

        for i in range(0, self.num_previous_speed):
            self.previous_speed_array.append(1000000.0)

    def run(self, current_speed_ms, target_speed_ms):
        if self.current_target_speed_ms != target_speed_ms:
            #self.traction_force = self.current_traction
            self.current_traction = self.max_traction

        self.current_target_speed_ms = target_speed_ms

        if current_speed_ms < target_speed_ms:
            self.traction_on(self.current_traction)

            if self.is_accelerating is True:
                self.current_traction = min(self.current_traction + 0.1, 100)
            else:
                self.current_traction = self.max_traction

            self.is_accelerating = True
        else:
            if current_speed_ms > target_speed_ms + target_speed_ms * 0.1:
                self.traction_off(self.current_traction)
            else:
                self.traction_off(0)

            if self.is_accelerating is False:
                self.current_traction = min(self.current_traction + 0.1, 100)
            else:
                self.current_traction = self.max_traction

            self.is_accelerating = False

            #self.traction_force -= 5

        self.previous_speed_array.pop(0)
        self.previous_speed_array.append(current_speed_ms)

        prev_speed = 1000000.0
        decelerate = True
        for s in self.previous_speed_array:
            if s <= prev_speed:
                prev_speed = s
                continue
            else:
                decelerate = False

        #if decelerate is True:
        #    self.traction_force += 5
        #    if self.traction_force > self.max_traction:
        #        self.traction_force = self.max_traction

    def forward(self):
        self.go_forward = True

    def backward(self):
        self.go_forward = False

    def traction_on(self, value):
        if self.go_forward is True:
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(value)
        else:
            Command.TRUCK_ACCELERATE(0)
            Command.TRUCK_BRAKE(value)

    def traction_off(self, value):
        if self.go_forward is False:
            Command.TRUCK_BRAKE(0)
            Command.TRUCK_ACCELERATE(value)
        else:
            Command.TRUCK_ACCELERATE(0)
            Command.TRUCK_BRAKE(value)

    def reset(self):
        Command.TRUCK_BRAKE(0)
        Command.TRUCK_ACCELERATE(0)
        self.__init__()
