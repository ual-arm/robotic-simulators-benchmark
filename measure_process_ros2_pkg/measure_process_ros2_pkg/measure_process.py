import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64, Float64MultiArray
import psutil
import numpy as np

class Process():
    def __init__(self, parent, id, topic, cmdline):
        self.id = id
        self.cmdline_arg_match = cmdline
        self.value = 0.0
        self.node = parent
        self.node.get_logger().warn('Init %s (cmdline args: "%s")' % (self.id, cmdline))
        self.pub_process_measure_ = self.node.create_publisher(Float64, topic.replace("-","_"), 10)


def split_process_arg(name : str):
    return name.split('@')


class MeasureProcess(Node):
    def __init__(self):
        super().__init__('measure_process')
        # Params
        self.declare_parameter('process_name', 'python3@ros2')
        self.declare_parameter('process_period', 0.5)

        # Subscription
        self.status_ = self.create_subscription(String, 'status', self.status_callback, 10)
        
        # Publisher
        self.pub_cpu_measure_ = self.create_publisher(Float64MultiArray, 'cpu_stats', 10)

        # Variables
        self.value = 0.0

        #
        self.initialize()
        
    def initialize(self):
        self.get_logger().info('Measure Process::inicialize() ok.')
        # Read Params
        self.process_name = self.get_parameter('process_name').get_parameter_value().string_value
        self.proc_list = self.process_name.split(', ')
        print(self.proc_list)
        self.process_list = list()
        for process in self.proc_list:
            lst = split_process_arg(process)
            process = lst[0]
            if len(lst) > 1: 
                cmdline = lst[1]
            else:
                cmdline = ''
                
            print('process: ' + process + ' cmdline: ' + str(cmdline))
            proc = Process(self, process, process+'_cpu', cmdline)
            self.process_list.append(proc)
        process_period = self.get_parameter('process_period').get_parameter_value().double_value

        self.timer = self.create_timer(process_period, self.iterate)

    def status_callback(self, msg):
        self.get_logger().info('Status: "%s"' % msg.data)

    def do_measure(self):
        pi = psutil.process_iter()
        # print(psutil.cpu_percent(percpu=True))

        for proc in pi:
            value =  proc.cpu_percent()
            for process in self.process_list:
                if not proc.name().__contains__(process.id):
                    continue
                anyCli = False
                for s in proc.cmdline():
                    if process.cmdline_arg_match in s:
                        anyCli = True

                if (process.cmdline_arg_match == '') or (anyCli): # check optional cli argument filter
                    process.value += value
                        
        msg = Float64MultiArray()
        for process in self.process_list:
            msg.data.append(process.value)
            self.get_logger().debug('Process %s = %f' % (process.id, process.value))
            process.value = 0.0

        self.get_logger().debug('Msg: %s' % str(msg))
        self.pub_cpu_measure_.publish(msg)


    def iterate(self):
        self.do_measure()

def main(args=None):
    rclpy.init(args=args)
    measure_process_node = MeasureProcess()
    rclpy.spin(measure_process_node)

    measure_process_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
