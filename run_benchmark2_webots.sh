#!/bin/bash

ros2 launch benchmark_webots turtlebot.launch.py &
ros2 launch small_robot_gazebo just_measure.launch.py

pkill SIGINT ros2
pkill SIGINT ros2
