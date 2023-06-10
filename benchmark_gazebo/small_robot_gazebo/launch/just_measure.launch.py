import os
import launch
import launch_ros
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    general_package_dir = get_package_share_directory('small_robot_gazebo')
    
    cpu_measure = Node(
        package='measure_process_ros2_pkg',
        executable='measure_process',
        name='benchmark',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'process_name' : 'gzserver, gzclient, mvsim_node, webots-bin, driver, python3@ros2_supervisor',
             'process_period' : 1.0},
        ],
    )
    
    stats_recorder_gzserver = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_gzserver',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_gzserver.txt',
             'initial_delay' : 20,
             'number_samples' : 60,
             'topic_array_index' : 0  # Index within "process_name[]" of measure_process
             },
        ],
    )
    stats_recorder_gzclient = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_gzclient',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_gzclient.txt',
             'initial_delay' : 20,
             'number_samples' : 60,
             'topic_array_index' : 1  # Index within "process_name[]" of measure_process
             },
        ],
    )

    stats_recorder_mvsim = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_mvsim',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_mvsim.txt',
             'initial_delay' : 10,
             'number_samples' : 60,
             'topic_array_index' : 2  # Index within "process_name[]" of measure_process
             },
        ],
    )

    stats_recorder_webots1 = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_webots',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_webots_bin.txt',
             'initial_delay' : 10,
             'number_samples' : 60,
             'topic_array_index' : 3  # Index within "process_name[]" of measure_process
             },
        ],
    )
    stats_recorder_webots2 = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_webots2',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_webots_driver.txt',
             'initial_delay' : 10,
             'number_samples' : 60,
             'topic_array_index' : 4  # Index within "process_name[]" of measure_process
             },
        ],
    )
    stats_recorder_webots1 = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_webots3',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_webots_ros2.txt',
             'initial_delay' : 10,
             'number_samples' : 60,
             'topic_array_index' : 5  # Index within "process_name[]" of measure_process
             },
        ],
    )
    
    ld = LaunchDescription()
    ld.add_action(cpu_measure)
    ld.add_action(stats_recorder_gzserver)
    ld.add_action(stats_recorder_gzclient)
    ld.add_action(stats_recorder_mvsim)
    ld.add_action(stats_recorder_webots1)
    ld.add_action(stats_recorder_webots2)
    ld.add_action(stats_recorder_webots3)

    return ld
