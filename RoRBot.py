#!/usr/bin/python3

import time
import Config
import Command
import Input
import sys
import Mode

Config.init(sys.argv[1])
Command.init()
Input.init()

print("Waiting for user activation")
while Input.is_started() is False:
    time.sleep(0.1)

Mode.init()

while True:
    Command.start_get_position()

    Mode.run()

    Command.stop_get_position()
