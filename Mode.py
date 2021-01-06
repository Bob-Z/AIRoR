import Config
import ModeRandom
import sys


def init():
    if Config.config['mode'] == 'random':
        ModeRandom.init()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()


def run():
    if Config.config['mode'] == 'random':
        ModeRandom.run()
    else:
        print('Unknown mode ' + Config.config['mode'])
        sys.exit()
