#!/usr/bin/env python3

# Usage example:
#
# ./measure-process.py --process mvsim
#
# ./measure-process.py --process gzserver --process gzclient   # sums both

import psutil
import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--process", type=str,
                    help="name of the process to measure", required=True, action='append')
parser.add_argument("--period", type=float,
                    help="period in seconds to wait for the measure (<1 second is ok)", required=False, default=0.5)

args = parser.parse_args()

val = 0


def do_measure():
    global val
    pi = psutil.process_iter()
    lst = {}
    for proc in pi:
        if not proc.name() in args.process:
            continue

        # We need to call this twice to get a first meaningful value
        val += proc.cpu_percent()


do_measure()
time.sleep(args.period)
do_measure()
print(val)
