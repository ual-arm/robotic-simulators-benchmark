# paper-emcr2023

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

## Use
Gazebo
```
ros2 launch small_robot_gazebo multi_small_robot.launch.py
```

- Physics: T=1 ms
- ROS Odom: 100 Hz
- ROS publish joint_state: 30 Hz (not used for us)
- Lidar: 200 rays, 360 deg, range 1.0 to 5.0 m. 100 Hz. Published to ROS.


Webots
```
ros2 launch mvsim_benchmark_webots multi_robot.launch.py
```
