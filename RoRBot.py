#!/usr/bin/python3

import sys
import time

import Command
import Config
import Input
import Mode
import Traction

Config.init(sys.argv[1])
Command.init()

Input.init()

print("Waiting for user activation")
while Input.is_started() is False:
    time.sleep(0.1)

Mode.init()
Traction.init()

Mode.run()
