#!/bin/bash

# Usage: Build and "source install/setup.bash" this repo with ROS2 & colcon first.
#        Then invoke this script.

rm /tmp/cpu*

for WITH_GUI in False True; do
    for N in {1..25..2}; do
    clear
    echo "========================================================"
    echo " LAUNCHING BENCHMARK FOR $N ROBOTS  (GUI: $WITH_GUI)    "
    echo "========================================================"

    BENCHMARK_GUI=$WITH_GUI BENCHMARK_NUM_ROBOTS=$N ros2 launch benchmark_mvsim multi_small_robot.launch.py
    sleep 2
    done
done

mkdir -p ./results/benchmark_n_robots
mv -v /tmp/cpu*.txt ./results/benchmark_n_robots
