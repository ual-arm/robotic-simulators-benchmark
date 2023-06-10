#!/bin/bash

# Usage: Build and "source install/setup.bash" this repo with ROS2 & colcon first.
#        Then invoke this script.

rm /tmp/cpu*

for WITH_GUI in True; do
    for N in {1..25..2}; do
    clear
    echo "========================================================"
    echo " LAUNCHING BENCHMARK FOR $N ROBOTS  (GUI: True)    "
    echo "========================================================"

    BENCHMARK_NUM_ROBOTS=$N ros2 launch benchmark_webots multi_robot.launch.py
    sleep 2
    done
done

mkdir -p ./results/benchmark_n_robots
mv -v /tmp/cpu*.txt ./results/benchmark_n_robots
