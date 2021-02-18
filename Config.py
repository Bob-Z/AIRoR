import json

config = None
file_name = None


def init(filename):
    global config
    global file_name

    file_name = filename

    with open(file_name) as f:
        config = json.load(f)


def save():
    global config
    global file_name

    with open(file_name, "w") as f:
        json.dump(config, f)
