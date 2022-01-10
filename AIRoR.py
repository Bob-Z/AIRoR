#!/usr/bin/python3

import sys
import time

import Command
import Config
import Input
import Mode

Config.init(sys.argv[2])
Command.init()

Input.init()

mode = Mode.Mode()
mode.run()
