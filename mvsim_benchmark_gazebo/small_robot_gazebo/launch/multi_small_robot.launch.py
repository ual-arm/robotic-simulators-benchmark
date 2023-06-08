import os
import launch
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration
from launch.actions import ExecuteProcess

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

def generate_launch_description():
    general_package_dir = get_package_share_directory('small_robot_gazebo')
    rviz_config_path = os.path.join(general_package_dir, 'rviz', 'test.rviz')
    use_sim_time = LaunchConfiguration('use_sim_time', default=True)
    model_dir = get_package_share_directory('small_robot_description')

    world_path = os.path.join(general_package_dir, 'worlds', 'Empty.world')
    
    show_gui = str2bool(os.getenv('BENCHMARK_GUI', 'False'))
    num_robots = int(os.getenv('BENCHMARK_NUM_ROBOTS', 1))
    
    if (show_gui):
        gzCmd = 'gazebo'
    else:
        gzCmd = 'gzserver'
    
    gazebo = ExecuteProcess(cmd=[gzCmd, '--verbose', world_path, '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', '--ros-args',
        ], output='screen'
    )
    lim = 10.0
    robot_node_list = []
    
    for i in range(num_robots):
        robot_name = 'small_robot{:02d}.urdf'.format(i)
        urdf_path = os.path.join(model_dir, 'urdf', robot_name)
        # fixed pos: avoid collisions
        x_pos = -lim + (i % 8)*2.5  #round(random.uniform(-lim, lim), 2)
        y_pos = -lim + (i/8)*2.5 #round(random.uniform(-lim, lim), 2)
        robot_node_list.append(Node(package='small_robot_gazebo', executable='inject_entity.py', output='screen',
                                            arguments=[urdf_path, str(x_pos), str(y_pos), '0.05', '0']),
        )

    
    #robot_state_publisher = Node(
    #    package='robot_state_publisher',
    #    executable='robot_state_publisher',
    #    output='screen',
    #    parameters=[{
    #        'robot_description': '<robot name=""><link name=""/></robot>'
    #    }],
    #)

    #rqt_node = Node(
    #    package='rqt_gui',
    #    executable='rqt_gui',
    #    name='interface',
    #    parameters=[
    #        {'use_sim_time': use_sim_time},
    #    ],
    #)

    #rviz_node = Node(
    #    package='rviz2',
    #    executable='rviz2',
    #    name='rviz2',
    #    output='screen',
    #    parameters=[
    #        {'use_sim_time': use_sim_time},
    #    ],
    #    arguments=['-d', rviz_config_path],
    #)

    cpu_measure = Node(
        package='measure_process_ros2_pkg',
        executable='measure_process',
        name='benchmark',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'process_name' : 'gzserver, ros2, rviz2, gzclient',
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
             'output_file' : '/tmp/cpu_gzserver_gui_{}_{:02d}.txt'.format(show_gui, num_robots),
             'initial_delay' : 20,
             'number_samples' : 30,
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
             'output_file' : '/tmp/cpu_gzclient_gui_{}_{:02d}.txt'.format(show_gui, num_robots),
             'initial_delay' : 20,
             'number_samples' : 30,
             'topic_array_index' : 3  # Index within "process_name[]" of measure_process
             },
        ],
    )
    
    ld = LaunchDescription()
    ld.add_action(gazebo)
    #ld.add_action(rqt_node)
    #ld.add_action(rviz_node)
    ld.add_action(cpu_measure)
    ld.add_action(stats_recorder_gzserver)
    ld.add_action(stats_recorder_gzclient)
    for robot in robot_node_list:
        ld.add_action(robot)

    return ld 
        