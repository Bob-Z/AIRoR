import Config
import ModeTruckRandom
import ModeTruckWaypoint
import ModeBoatWaypoint
import ModeHeliWaypoint
import sys
import threading
import time
import Command
import Traction
import Throttle


def init():
    thread = threading.Thread(target=get_position)
    thread.start()

    if Config.config['mode'] == 'truck_random':
        ModeTruckRandom.init()
        Traction.init()
    elif Config.config['mode'] == 'truck_waypoint':
        ModeTruckWaypoint.init()
        Traction.init()
    elif Config.config['mode'] == 'boat_waypoint':
        ModeBoatWaypoint.init()
        Throttle.init()
    elif Config.config['mode'] == 'heli_waypoint':
        ModeHeliWaypoint.init()
        Throttle.init()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()


def run():
    if Config.config['mode'] == 'truck_random':
        ModeTruckRandom.run()
    elif Config.config['mode'] == 'truck_waypoint':
        ModeTruckWaypoint.run()
    elif Config.config['mode'] == 'boat_waypoint':
        ModeBoatWaypoint.run()
    elif Config.config['mode'] == 'heli_waypoint':
        ModeHeliWaypoint.run()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()


def get_position():
    while True:
        Command.start_get_position()
        time.sleep(0.05)
        Command.stop_get_position()
        time.sleep(0.05)
