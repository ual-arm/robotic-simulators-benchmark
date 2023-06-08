#!/bin/bash

# Usage: Build and "source install/setup.bash" this repo with ROS2 & colcon first.
#        Then invoke this script.

rm /tmp/cpu*

for WITH_GUI in False True; do
    for N in {1..25..4}; do
    clear
    echo "========================================================"
    echo " LAUNCHING BENCHMARK FOR $N ROBOTS  (GUI: $WITH_GUI)    "
    echo "========================================================"

    BENCHMARK_GUI=$WITH_GUI BENCHMARK_NUM_ROBOTS=$N ros2 launch mvsim_benchmark_mvsim multi_small_robot.launch.py
    done
done

mkdir -p ./benchmark1_results
mv -v /tmp/cpu*.txt ./benchmark1_results
