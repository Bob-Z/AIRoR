import Config


class SaveAvoid:
    def __init__(self):
        pass

    def run(self):
        pass

    def reset(self, position):
        if 'avoid' not in Config.save_json:
            Config.save_json['avoid'] = []

        Config.save_json['avoid'].append(position)

        Config.save()

        self.__init__()
