#!/bin/bash

export 

for WITH_GUI in False True; do
    clear
    echo "========================================================"
    echo " LAUNCHING BENCHMARK FOR TURTLEBOT  (GUI: $WITH_GUI)    "
    echo "========================================================"

    BENCHMARK_GUI=$WITH_GUI TURTLEBOT3_MODEL=burger ros2 launch small_robot_gazebo turtlebot_benchmark.launch.py
    done
done

mkdir -p ./results/benchmark_turtlebot
mv -v /tmp/cpu*.txt ./results/benchmark_turtlebot
