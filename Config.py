import json

conf_file_name = None
save_file_name = None
config_json = None
save_json = {}


def init(filename):
    global conf_file_name
    global save_file_name
    global config_json
    global save_json

    conf_file_name = filename
    save_file_name = filename + ".save.json"

    try:
        with open(conf_file_name) as f:
            config_json = json.load(f)
        print("Configuration file", conf_file_name, "load OK")
    except FileNotFoundError:
        print("Cannot find configuration file:", conf_file_name)
        exit(1)

    try:
        with open(save_file_name) as f:
            save_json = json.load(f)
        print("Save file", conf_file_name, "load OK")
    except FileNotFoundError:
        print("No save file for ", conf_file_name)


def save():
    global save_json
    global save_file_name

    with open(save_file_name, "w") as f:
        json.dump(save_json, f)
