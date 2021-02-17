class TargetNone:
    def __init__(self):
        pass

    def run(self, position, rotation, speed_ms):
        return 0.0, 0.0, 0.0

    def reset(self):
        self.__init__()
