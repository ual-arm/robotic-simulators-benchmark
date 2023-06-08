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
    general_package_dir = get_package_share_directory('mvsim_benchmark_mvsim')
    mvsimDir = get_package_share_directory("mvsim")

    world_path = os.path.join(general_package_dir, 'worlds', 'simple-room.world.xml')
    
    show_gui = str2bool(os.getenv('BENCHMARK_GUI', 'False'))
    
    # Number of robots is handled directly inside the MVSim world XML file.
    num_robots = int(os.getenv('BENCHMARK_NUM_ROBOTS', 1))
    
    mvsim_node = Node(
        package='mvsim',
        executable='mvsim_node',
        name='mvsim',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[
            os.path.join(mvsimDir, 'mvsim_tutorial',
                         'mvsim_ros2_params.yaml'),
            {
                "world_file": world_path,
                "headless": not show_gui,
            }]
    )

    cpu_measure = Node(
        package='measure_process_ros2_pkg',
        executable='measure_process',
        name='benchmark',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'process_name' : 'mvsim_node',
             'process_period' : 1.0},
        ],
    )
    
    stats_recorder_mvsim = Node(
        package='measure_process_ros2_pkg',
        executable='record_cpu_usage',
        name='stats_recorder_mvsim',
        output='screen',
        on_exit=launch.actions.Shutdown(),
        parameters=[{
             'output_file' : '/tmp/cpu_mvsim_gui_{}_{:02d}.txt'.format(show_gui, num_robots),
             'initial_delay' : 6,
             'number_samples' : 30,
             'topic_array_index' : 0  # Index within "process_name[]" of measure_process
             },
        ],
    )
    
    ld = LaunchDescription()
    ld.add_action(mvsim_node)
    ld.add_action(cpu_measure)
    ld.add_action(stats_recorder_mvsim)

    return ld 
        