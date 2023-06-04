import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64, Float64MultiArray
import psutil
import numpy as np

class Process():
    def __init__(self, parent, id, topic):
        self.id = id
        self.value = 0.0
        self.node = parent
        self.node.get_logger().warn('Init %s' % (self.id))
        self.pub_process_measure_ = self.node.create_publisher(Float64, topic.replace("-","_"), 10)

class MeasureProcess(Node):
    def __init__(self):
        super().__init__('measure_process')
        # Params
        self.declare_parameter('process_name', 'gzserver')
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
            proc = Process(self, process, process+'_cpu')
            self.process_list.append(proc)
        process_period = self.get_parameter('process_period').get_parameter_value().double_value

        self.timer = self.create_timer(process_period, self.iterate)

    def status_callback(self, msg):
        self.get_logger().info('Status: "%s"' % msg.data)

    def do_measure(self):
        data_list = list()
        cpu_count = psutil.cpu_count()
        data_list.append(float(cpu_count))
        data_list.append(psutil.cpu_percent(interval=None))
        mem = psutil.virtual_memory()
        data_list.append(mem.percent)
        load_tuple = psutil.getloadavg()
        for load in load_tuple:
            percent = (load / cpu_count) * 100
            data_list.append(percent)

        msg = Float64MultiArray()
        msg.data = data_list
        self.pub_cpu_measure_.publish(msg)
        pi = psutil.process_iter()

        # print(psutil.cpu_percent(percpu=True))

        for proc in pi:
            if not proc.name() in self.proc_list:
                continue

            value =  proc.cpu_percent()
            for process in self.process_list:
                if proc.name() == process.id:
                    process.value += value
        
        msg = Float64()
        for process in self.process_list: 
            msg.data = process.value
            process.pub_process_measure_.publish(msg)
            self.get_logger().debug('Process %s = %f' % (process.id, msg.data))
            process.value = 0.0


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
