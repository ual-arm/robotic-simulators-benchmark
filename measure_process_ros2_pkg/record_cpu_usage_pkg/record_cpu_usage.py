import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64, Float64MultiArray

class RecordCpuUsage(Node):
    def __init__(self):
        super().__init__('record_cpu_usage')
        # Params
        self.declare_parameter('output_file', '/tmp/cpu.txt')
        self.declare_parameter('initial_delay', 10.0)  # [s]
        self.declare_parameter('number_samples', 30)
        self.declare_parameter('topic_name', cpu_stats)

       
        # Variables
        self.value = 0.0

        #
        self.initialize()
        
    def initialize(self):
        self.get_logger().info('RecordCpuUsage::inicialize() ok.')
        # Read Params
        self.output_file = self.get_parameter('output_file').get_parameter_value().string_value
        
        # Subscription
        self.sub_cpu_ = self.create_subscription(Float64MultiArray, 'cpu_stats', self.cpu_callback, 10)

    def cpu_callback(self, msg):
        self.get_logger().info('cpu_callback: "%s"' % msg.data)


    def iterate(self):
        # xxx

def main(args=None):
    rclpy.init(args=args)
    node = RecordCpuUsage()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
