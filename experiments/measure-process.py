#!/usr/bin/env python3

import psutil
import time


PROCESS_NAME = 'mvsim'
val = 0


def do_measure():
    global val
    pi = psutil.process_iter()
    lst = {}
    for proc in pi:
        if proc.name() != PROCESS_NAME:
            continue

        # We need to call this twice to get a first meaningful value
        val = proc.cpu_percent()
        break


do_measure()
time.sleep(0.5)
do_measure()
print(val)
