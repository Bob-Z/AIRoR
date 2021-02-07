import Command


class HeliHeight:
    def __init__(self):
        self.previous_height = 0.0
        self.event_ahead_qty = 10
        pass

    def event(self, position, rotation, waypoint):
        height_since_previous_event = self.previous_height - position[1]
        next_height = position[1] - (self.event_ahead_qty * height_since_previous_event)

        self.previous_height = position[1]

        if next_height < waypoint[1]:
            Command.stop_command_2()
            Command.start_command_1()
        else:
            Command.stop_command_1()
            Command.start_command_2()
