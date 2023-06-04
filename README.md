# Robotic simulators benchmark

The goal of this repository is to provide a common set of scenarios/robots/sensors 
such that they are all simulated in different mobile robot simulators for CPU-usage benchmarking.

## Requisites

- Install: 
  - gazebo
  - Webots
  - Webots ROS2 pkg `sudo apt-get install ros-$ROS_DISTRO-webots-ros2`

Python packages:

    sudo pip install transformations    # or local to the user


## Build
Para contruir el .urdf de los robots, editar el límite del "foreach" del fichero [CMakeList](https://github.com/FranciscoJManasAlvarez/paper-emcr2023/blob/f5d9632c52c9b0dbd2676620fd8f732cf919dfdf/experiments/mvsim_benchmark_gazebo/small_robot_description/CMakeLists.txt#L30) y luego el bucle for del [launch](https://github.com/FranciscoJManasAlvarez/paper-emcr2023/blob/f5d9632c52c9b0dbd2676620fd8f732cf919dfdf/experiments/mvsim_benchmark_gazebo/small_robot_gazebo/launch/multi_small_robot.launch.py#L23)
```
colcon build --symlink-install && source install/setup.bash
```

## Run benchmark 1

### Conditions

- Many robots (N=1 to 25), simple empty square room.
- Physics: T=1 ms
- ROS Odom: 100 Hz
- ROS publish joint_state: 30 Hz (not used here)
- Lidar: 200 rays, 360 deg, range 1.0 to 5.0 m. Sensor rate: 20 Hz. Published to ROS.


### Gazebo

```
BENCHMARK_GUI=False BENCHMARK_NUM_ROBOTS=10  ros2 launch small_robot_gazebo multi_small_robot.launch.py
```


### Webots

```
ros2 launch mvsim_benchmark_webots multi_robot.launch.py
```

### MVSim

```
ros2 launch xxx
```

## Run benchmark 2: turtlebot3 world

### Gazebo

```
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

### MVSim

```
ros2 launch  mvsim demo_turtlebot_world.launch.py
```
