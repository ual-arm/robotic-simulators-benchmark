#!/bin/bash

ros2 launch mvsim demo_turtlebot_world.launch.py &
ros2 launch small_robot_gazebo just_measure.launch.py

pkill SIGINT ros2
pkill SIGINT ros2
