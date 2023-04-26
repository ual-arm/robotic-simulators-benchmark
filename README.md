# paper-emcr2023

## Build
Para contruir el .urdf de los robots, editar el límite del "foreach" del fichero [CMakeList](https://github.com/FranciscoJManasAlvarez/paper-emcr2023/blob/f5d9632c52c9b0dbd2676620fd8f732cf919dfdf/experiments/mvsim_benchmark_gazebo/small_robot_description/CMakeLists.txt#L30) y luego el bucle for del [launch](https://github.com/FranciscoJManasAlvarez/paper-emcr2023/blob/f5d9632c52c9b0dbd2676620fd8f732cf919dfdf/experiments/mvsim_benchmark_gazebo/small_robot_gazebo/launch/multi_small_robot.launch.py#L23)
```
colcon build --symlink-install && source install/setup.bash
```

## Use
```
ros2 launch small_robot_gazebo multi_small_robot.launch.py
```
