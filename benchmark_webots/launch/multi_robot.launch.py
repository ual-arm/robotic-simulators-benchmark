import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.substitutions.path_join_substitution import PathJoinSubstitution
from launch import LaunchDescription
from webots_ros2_driver.webots_launcher import WebotsLauncher
from webots_ros2_driver.utils import controller_url_prefix

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def get_ros2_nodes(*args):
    package_dir = get_package_share_directory('benchmark_webots')
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'robot.urdf')).read_text()
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    show_gui = str2bool(os.getenv('BENCHMARK_GUI', 'False'))

    # Number of robots
    num_robots = int(os.getenv('BENCHMARK_NUM_ROBOTS', 1))

    robot_node_list = []

    for i in range(num_robots):
        if i<10:
            robot_name = 'small_robot0'+str(i)
        else:
            robot_name = 'small_robot'+str(i)
        
        robot_node_list.append(Node(package='webots_ros2_driver',
                                    executable='driver',
                                    output='screen',
                                    additional_env={'WEBOTS_ROBOT_NAME': robot_name,
                                                    'WEBOTS_CONTROLLER_URL': controller_url_prefix() + robot_name},
                                    parameters=[{   'robot_description': robot_description,
                                                    'use_sim_time': use_sim_time},
                                    ]
                                )
        )

    robot_node_list.append(Node(
            package='measure_process_ros2_pkg',
            executable='measure_process',
            name='benchmark',
            output='screen',
            parameters=[{
                'process_name' : 'webots-bin, driver, python3@ros2_supervisor',
                'process_period' : 1.0},
            ],
        )
    )

    robot_node_list.append(Node(
            package='measure_process_ros2_pkg',
            executable='record_cpu_usage',
            name='stats_recorder_webots',
            output='screen',
            on_exit=launch.actions.Shutdown(),
            parameters=[{
                'output_file' : '/tmp/cpu_webots_bin_{:02d}.txt'.format(num_robots),
                'initial_delay' : 10,
                'number_samples' : 60,
                'topic_array_index' : 0  # Index within "process_name[]" of measure_process
                },
            ],
        )
    )
    robot_node_list.append(Node(
            package='measure_process_ros2_pkg',
            executable='record_cpu_usage',
            name='stats_recorder_webots',
            output='screen',
            on_exit=launch.actions.Shutdown(),
            parameters=[{
                'output_file' : '/tmp/cpu_webots_bin_{:02d}.txt'.format(num_robots),
                'initial_delay' : 10,
                'number_samples' : 60,
                'topic_array_index' : 1  # Index within "process_name[]" of measure_process
                },
            ],
        )
    )
    robot_node_list.append(Node(
            package='measure_process_ros2_pkg',
            executable='record_cpu_usage',
            name='stats_recorder_webots',
            output='screen',
            on_exit=launch.actions.Shutdown(),
            parameters=[{
                'output_file' : '/tmp/cpu_webots_bin_{:02d}.txt'.format(num_robots),
                'initial_delay' : 10,
                'number_samples' : 60,
                'topic_array_index' : 2  # Index within "process_name[]" of measure_process
                },
            ],
        )
    )

    return robot_node_list

def generate_launch_description():
    package_dir = get_package_share_directory('benchmark_webots')
    world = LaunchConfiguration('world')
    mode = LaunchConfiguration('mode')
    webots = WebotsLauncher(
        world=PathJoinSubstitution([package_dir, 'worlds', world]),
        mode=mode,
        ros2_supervisor=True
    )

    reset_handler = launch.actions.RegisterEventHandler(
        event_handler=launch.event_handlers.OnProcessExit(
            target_action=webots._supervisor,
            on_exit=get_ros2_nodes,
        )
    )

    num_robots = int(os.getenv('BENCHMARK_NUM_ROBOTS', 1))

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='N'+str(num_robots)+'_world.wbt',
            description='Benchmark World'
        ),
        DeclareLaunchArgument(
            'mode',
            default_value='realtime',
            description='Webots startup mode'
        ),
        webots,
        webots._supervisor,

        # This action will kill all nodes once the Webots simulation has exited
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[
                    launch.actions.UnregisterEventHandler(
                        event_handler=reset_handler.event_handler
                    ),
                    launch.actions.EmitEvent(event=launch.events.Shutdown())
                ],
            )
        ),

        # Add the reset event handler
        reset_handler
    ] + get_ros2_nodes())

