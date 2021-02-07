import Command
import Math


class HeliDirection:
    def __init__(self):
        self.previous_diff_target = 0.0
        self.event_ahead_qty = 3
        self.previous_rotation_since_previous_event = 0.0
        # self.fixed_rotation = "none"
        pass

    def event(self, position, rotation, waypoint):
        waypoint_angle = Math.calc_angle([position[0], position[2] + 1.0], [position[0], position[2]],
                                         [waypoint[0], waypoint[2]])

        if waypoint_angle > 0:
            target_angle = waypoint_angle - 180.0
        else:
            target_angle = waypoint_angle + 180.0

        diff_target = rotation[1] - target_angle
        diff_target = diff_target % 360

        if diff_target > 180.0:
            diff_target = diff_target - 360.0
        if diff_target < -180.0:
            diff_target = 360.0 + diff_target

        diff_target_since_previous_event = self.previous_diff_target - diff_target

        next_diff_target = diff_target - (self.event_ahead_qty * diff_target_since_previous_event)

        self.previous_diff_target = diff_target

        next_diff_target = next_diff_target % 360

        if next_diff_target > 180.0:
            next_diff_target = next_diff_target - 360.0
        if next_diff_target < -180.0:
            next_diff_target = 360.0 + next_diff_target

        print("diff_target = ", diff_target)
        print("next_diff_target = ", next_diff_target)

        if next_diff_target > 0:
                print("Go left")
                Command.TRUCK_STEER_LEFT(diff_target + 10.0)
        elif next_diff_target < 0:
                print("Go right")
                Command.TRUCK_STEER_RIGHT(diff_target + 10.0)
        else:
            print("Go nowhere")
