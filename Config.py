import json

config = None


def init(file_name):
    global config
    with open(file_name) as f:
        config = json.load(f)

    print("Mode: " + config['mode'])
