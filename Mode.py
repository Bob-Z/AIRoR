import Config
import ModeTruckRandom
import ModeTruckWaypoint
import sys
import threading
import time
import Command


def init():
    thread = threading.Thread(target=get_position)
    thread.start()

    if Config.config['mode'] == 'truck_random':
        ModeTruckRandom.init()
    elif Config.config['mode'] == 'truck_waypoint':
        ModeTruckWaypoint.init()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()


def run():
    if Config.config['mode'] == 'truck_random':
        ModeTruckRandom.run()
    elif Config.config['mode'] == 'truck_waypoint':
        ModeTruckWaypoint.run()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()


def get_position():
    while True:
        Command.start_get_position()
        time.sleep(0.1)
        Command.stop_get_position()
