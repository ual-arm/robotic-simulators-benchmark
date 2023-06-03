import os
import random
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess

def generate_launch_description():
    general_package_dir = get_package_share_directory('small_robot_gazebo')
    rviz_config_path = os.path.join(general_package_dir, 'rviz', 'test.rviz')
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    model_dir = get_package_share_directory('small_robot_description')

    world_path = os.path.join(general_package_dir, 'worlds', 'Empty.world')
    
    show_gui = True
    
    if (show_gui):
        gzCmd = 'gazebo'
    else:
        gzCmd = 'gzserver'
    
    gazebo = ExecuteProcess(cmd=[gzCmd, '--verbose', world_path, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', '--ros-args',
        ], output='screen'
    )
    lim = 10.0
    robot_node_list = []
    
    for i in range(15):
        if i<10:
            robot_name = 'small_robot0'+str(i)+'.urdf'
        else:
            robot_name = 'small_robot'+str(i)+'.urdf'
        urdf_path = os.path.join(model_dir, 'urdf', robot_name)
        x_pos = round(random.uniform(-lim, lim), 2)
        y_pos = round(random.uniform(-lim, lim), 2)
        robot_node_list.append(Node(package='small_robot_gazebo', executable='inject_entity.py', output='screen',
                                            arguments=[urdf_path, str(x_pos), str(y_pos), '0.05', '0']),
        )

    
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': '<robot name=""><link name=""/></robot>'
        }],
    )

    rqt_node = Node(
        package='rqt_gui',
        executable='rqt_gui',
        name='interface',
        parameters=[
            {'use_sim_time': use_sim_time},
        ],
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
        ],
        arguments=['-d', rviz_config_path],
    )

    cpu_measure = Node(
        package='measure_process_ros2_pkg',
        executable='measure_process',
        name='benchmark',
        output='screen',
        parameters=[{
             'process_name' : 'gzserver, ros2, rviz2, gzclient',
             'process_period' : 0.5},
        ],
    )
    
    ld = LaunchDescription()
    ld.add_action(gazebo)
    ld.add_action(rqt_node)
    ld.add_action(rviz_node)
    ld.add_action(cpu_measure)
    for robot in robot_node_list:
        ld.add_action(robot)

    return ld 
        