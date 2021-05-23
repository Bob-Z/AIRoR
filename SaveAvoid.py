import Config


class SaveAvoid:
    def __init__(self):
        pass

    def run(self):
        pass

    def reset(self, position):
        if 'avoid' not in Config.config:
            Config.config['avoid'] = []

        Config.config['avoid'].append(position)

        Config.save()

        self.__init__()
