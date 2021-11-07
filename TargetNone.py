class TargetNone:
    def __init__(self):
        pass

    def run(self, position, rotation, speed_ms, rot_diff, target_speed_ms, go_up):
        return 0.0, 0.0, 0.0

    def reset(self):
        self.__init__()
