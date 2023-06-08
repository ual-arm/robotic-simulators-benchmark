import rclpy
import os
import time
from rclpy.node import Node
from std_msgs.msg import String, Float64, Float64MultiArray

class RecordCpuUsage(Node):
    def __init__(self):
        super().__init__('record_cpu_usage')
        # Params
        self.declare_parameter('output_file', '/tmp/cpu.txt')
        self.declare_parameter('initial_delay', 10)  # [s]
        self.declare_parameter('number_samples', 30)
        self.declare_parameter('topic_name', 'cpu_stats')
        self.declare_parameter('topic_array_index', 0)

       
        # Variables
        self.value = 0.0
        
        #
        self.initialize()

    def initialize(self):
        self.get_logger().info('RecordCpuUsage::inicialize() ok.')
        # Read Params
        self.output_file = self.get_parameter('output_file').get_parameter_value().string_value
        self.topic_array_index = self.get_parameter('topic_array_index').get_parameter_value().integer_value
        self.initial_delay = self.get_parameter('initial_delay').get_parameter_value().integer_value
        self.number_samples = self.get_parameter('number_samples').get_parameter_value().integer_value
        self.topic_name = self.get_parameter('topic_name').get_parameter_value().string_value
        
        self.iters_count = 0
        
        # Subscription
        self.sub_cpu_ = self.create_subscription(Float64MultiArray, self.topic_name, self.cpu_callback, 1)
        
        self.out_fil = open(self.output_file, 'wt')


    def cpu_callback(self, msg):
        pcCPU = msg.data[self.topic_array_index]
        
        self.iters_count += 1
        if (self.iters_count < self.initial_delay):
            return
        
        self.get_logger().info('cpu_callback: {}% [{} / {} / {}]'.format(pcCPU, self.iters_count, self.initial_delay, self.number_samples))
        self.out_fil.write(str(pcCPU) + '\n')

        if (self.iters_count >= self.number_samples + self.initial_delay):
            self.get_logger().info('ALL SAMPLES GRABBED. Shutting down')
            self.out_fil.close()
            time.sleep(1.0)
            os.system('pkill -SIGINT ros2')
            os.system('pkill -KILL gzclient')
            os.system('pkill -KILL gzserver')
            #launch.actions.Shutdown()

    def iterate(self):
        self.get_logger().info('iterate')



def main(args=None):
    rclpy.init(args=args)
    node = RecordCpuUsage()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
