import Config


class SaveMap:
    def __init__(self):
        pass

    def run(self):
        pass

    def reset(self, position):
        if 'map' not in Config.config:
            Config.config['map'] = []

        Config.config['map'].append(position)

        Config.save()

        self.__init__()
