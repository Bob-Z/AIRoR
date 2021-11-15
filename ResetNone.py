class ResetNone:
    def __init__(self):
        pass

    def run(self, position, current_speed_ms):
        return False, None

    def reset(self):
        self.__init__()
