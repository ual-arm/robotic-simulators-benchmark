import os
import pathlib
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from webots_ros2_driver.webots_launcher import WebotsLauncher, Ros2SupervisorLauncher
from webots_ros2_driver.utils import controller_url_prefix

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def generate_launch_description():
    package_dir = get_package_share_directory('benchmark_webots')
    robot_description = pathlib.Path(os.path.join(package_dir, 'resource', 'robot.urdf')).read_text()
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)

    show_gui = str2bool(os.getenv('BENCHMARK_GUI', 'False'))

    # Number of robots
    num_robots = int(os.getenv('BENCHMARK_NUM_ROBOTS', 1))

    webots = WebotsLauncher(
        world=os.path.join(package_dir, 'worlds', 'N'+str(num_robots)+'_world.wbt')
    )

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
                                    parameters=[{   'robot_description': robot_description},
                                    ]
                                )
        )

    cpu_measure = Node(
        package='measure_process_ros2_pkg',
        executable='measure_process',
        name='benchmark',
        output='screen',
        parameters=[{
             'process_name' : 'webots-bin',
             'process_period' : 1.0},
        ],
    )

    stats_recorder_webots = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_webots',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_webots_gui_{}_{:02d}.txt'.format(show_gui, num_robots),
             'initial_delay' : 10,
             'number_samples' : 60,
             'topic_array_index' : 0  # Index within "process_name[]" of measure_process
             },
        ],
    )

    ros2_close = launch.actions.RegisterEventHandler(
                    event_handler=launch.event_handlers.OnProcessExit(
                    target_action=webots,
                    on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
                    )
                )


    ld = LaunchDescription()
    ld.add_action(webots)
    # ld.add_action(cpu_measure)
    # ld.add_action(stats_recorder_webots)
    for robot in robot_node_list:
        ld.add_action(robot)
        
    ld.add_action(ros2_close)

    return ld
