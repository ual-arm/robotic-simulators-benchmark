# Robotic simulators benchmark

The goal of this repository is to provide a common set of scenarios/robots/sensors 
such that they are all simulated in different mobile robot simulators for CPU-usage benchmarking.

## Requisites

- Install: 
  - MVSim: `sudo apt-get install ros-$ROS_DISTRO-mvsim`
  - Gazebo: `sudo apt-get install ros-$ROS_DISTRO-gazebo-ros`
  - Webots ROS2 pkg `sudo apt-get install ros-$ROS_DISTRO-webots-ros2`

Python packages:

    sudo pip install transformations    # or local to the user, venv, etc.

## Build

Clone this repo in a ROS 2 workspace directory as usual, e.g. `~/ros2_ws/src/` then build with colcon:

```
colcon build --symlink-install && source install/setup.bash
```

## Run benchmark 1

### Conditions

- Many robots (N=1 to 25), simple empty square room.
- Physics: T=10 ms  (Limit here was Webots; Gazebo and MVSim can run at T=1 ms).
- ROS Odom: 100 Hz
- ROS publish joint_state: 30 Hz (not used here)
- Lidar: 200 rays, 360 deg, range 1.0 to 5.0 m. Sensor rate: 20 Hz. Published to ROS.


### Gazebo

Individual run test:

    BENCHMARK_GUI=False BENCHMARK_NUM_ROBOTS=10  ros2 launch small_robot_gazebo multi_small_robot.launch.py

Complete benchmark:

    run_benchmark1_gazebo.sh

### Webots

Individual run test:

    BENCHMARK_NUM_ROBOTS=10 ros2 launch benchmark_webots multi_robot.launch.py

(No option to disable the GUI for Webots)

Complete benchmark:

    run_benchmark1_webots.sh

### MVSim

Individual run test:

    BENCHMARK_GUI=False BENCHMARK_NUM_ROBOTS=10  ros2 launch small_robot_gazebo multi_small_robot.launch.py
    
Complete benchmark:

    run_benchmark1_mvsim.sh

## Details
To rebuild the robots `.urdf`, edit the "foreach" in this [CMakeList](https://github.com/FranciscoJManasAlvarez/paper-emcr2023/blob/f5d9632c52c9b0dbd2676620fd8f732cf919dfdf/experiments/mvsim_benchmark_gazebo/small_robot_description/CMakeLists.txt#L30) and then the for loop in this [launch](https://github.com/FranciscoJManasAlvarez/paper-emcr2023/blob/f5d9632c52c9b0dbd2676620fd8f732cf919dfdf/experiments/mvsim_benchmark_gazebo/small_robot_gazebo/launch/multi_small_robot.launch.py#L23).


