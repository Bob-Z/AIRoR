import Config
import ModeRandom
import ModeWaypoint
import sys


def init():
    if Config.config['mode'] == 'random':
        ModeRandom.init()
    elif Config.config['mode'] == 'waypoint':
        ModeWaypoint.init()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()


def run():
    if Config.config['mode'] == 'random':
        ModeRandom.run()
    elif Config.config['mode'] == 'waypoint':
        ModeWaypoint.run()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()
