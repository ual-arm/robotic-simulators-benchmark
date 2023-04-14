import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64
import psutil
import time


class MeasureProcess(Node):
    def __init__(self):
        super().__init__('measure_process')
        # Params
        self.declare_parameter('process_name', 'webots-bin')
        self.declare_parameter('process_period', 0.5)

        # Subscription
        self.status_ = self.create_subscription(String, 'status', self.status_callback, 10)
        
        # Publisher
        self.pub_process_measure_ = self.create_publisher(Float64, 'process_value', 10)

        # Variables
        self.value = 0.0

        #
        self.initialize()
        
    def initialize(self):
        self.get_logger().info('Measure Process::inicialize() ok.')
        # Read Params
        self.process_name = self.get_parameter('process_name').get_parameter_value().string_value
        process_period = self.get_parameter('process_period').get_parameter_value().double_value

        self.timer = self.create_timer(process_period, self.iterate)

    def status_callback(self, msg):
        self.get_logger().info('Status: "%s"' % msg.data)

    def do_measure(self):
        pi = psutil.process_iter()
        lst = {}
        
        for proc in pi:
            if not proc.name() in self.process_name:
                continue

            # We need to call this twice to get a first meaningful value
            value =  proc.cpu_percent()
            if not value == 0.0:
                self.value = value
                self.get_logger().debug('Measure Process :: Value = %f' % self.value)

    def iterate(self):
        self.do_measure()
        msg = Float64()
        msg.data = self.value
        self.pub_process_measure_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    measure_process_node = MeasureProcess()
    rclpy.spin(measure_process_node)

    measure_process_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
