import json

config = None


def init(file_name):
    global config
    with open(file_name) as f:
        config = json.load(f)

    if 'mode' in config:
        print("Mode: " + config['mode'])
