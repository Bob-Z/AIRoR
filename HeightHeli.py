import Command


class HeightHeli:
    def __init__(self):
        print("Height mode: Helicopter")
        pass

    def run(self, go_up):
        if go_up is True:
            Command.stop_COMMANDS_02()
            Command.start_COMMANDS_01()
        else:
            Command.stop_COMMANDS_01()
            Command.start_COMMANDS_02()

    def reset(self):
        Command.stop_COMMANDS_01()
        Command.stop_COMMANDS_02()
