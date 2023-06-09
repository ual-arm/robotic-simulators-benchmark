import numpy as np
import os
import rclpy
from rclpy.node import Node
from rclpy.time import Time
import tf_transformations

from geometry_msgs.msg import Twist, Pose, Point, TransformStamped
from math import atan2, cos, sin, degrees, radians, pi, sqrt
from nav_msgs.msg import Odometry
from std_msgs.msg import String, Bool, Float64
from sensor_msgs.msg import LaserScan
from tf2_ros import TransformBroadcaster


HALF_DISTANCE_BETWEEN_WHEELS = 0.5
WHEEL_RADIUS = 0.2

class RobotDriver:
    def init(self, webots_node, properties):
        self.__robot = webots_node.robot
        timestep = int(self.__robot.getBasicTimeStep())

        ## Initialize motors
        self.__left_motor = self.__robot.getDevice('left wheel motor')
        self.__left_motor.setPosition(float('inf'))
        self.__left_motor.setVelocity(0)
        self.__right_motor = self.__robot.getDevice('right wheel motor')
        self.__right_motor.setPosition(float('inf'))
        self.__right_motor.setVelocity(0)
        

        ## Initialize Sensors
        self.__imu = self.__robot.getDevice("inertial unit")
        self.__imu.enable(timestep)
        self.__gps = self.__robot.getDevice("gps")
        self.__gps.enable(timestep)
        self.__gyro = self.__robot.getDevice("gyro")
        self.__gyro.enable(timestep)
        self.__lidar = self.__robot.getDevice("LDS-01")
        self.__lidar.enable(timestep)

        ## Intialize Variables
        self.__target_twist = Twist()

        # Init ROS2 Node
        self.name_value = os.environ['WEBOTS_ROBOT_NAME']
        rclpy.init(args=None)
        self.__node = rclpy.create_node(self.name_value+'_driver')
        # Subscription
        self.__node.create_subscription(Twist, '/cmd_vel', self.__cmd_vel_callback, 1)
        # Publisher
        self.__laser_publisher = self.__node.create_publisher(LaserScan, self.name_value+'/scan', 10)

        self.tfbr = TransformBroadcaster(self.__node)

        self.initialize()
    
    def initialize(self):
        self.__node.get_logger().info('Webots_Node::inicialize() ok. %s' % (str(self.name_value)))
        # Read Params

        #
        self.__node.create_timer(0.05, self.publish_laserscan_data)

    def publish_laserscan_data(self):
        ranges = self.__lidar.getLayerRangeImage(0)
        if ranges:
            self.msg_laser = LaserScan()
            self.msg_laser.header.stamp = Time(seconds=self.__robot.getTime()).to_msg()
            self.msg_laser.header.frame_id = self.name_value+'/base_link'
            self.msg_laser.angle_min = -self.__lidar.getFov()/2.0
            self.msg_laser.angle_max = self.__lidar.getFov()/2.0
            self.msg_laser.angle_increment = self.__lidar.getFov()/self.__lidar.getHorizontalResolution()
            self.msg_laser.time_increment = float(self.__lidar.getSamplingPeriod()) / (1000.0 * self.__lidar.getHorizontalResolution())
            self.msg_laser.scan_time = float(self.__lidar.getSamplingPeriod()) / 1000.0
            self.msg_laser.range_min = self.__lidar.getMinRange()
            self.msg_laser.range_max = self.__lidar.getMaxRange()
            self.msg_laser.ranges = ranges
            self.__laser_publisher.publish(self.msg_laser)

    def __cmd_vel_callback(self, twist):
        self.__target_twist = twist

    def step(self):
        rclpy.spin_once(self.__node, timeout_sec=0)
        # self.__node.get_logger().info('Webots_Node::iterate() ok. %s' % (str(self.name_value)))
        q = tf_transformations.quaternion_from_euler(self.__imu.getRollPitchYaw()[0], self.__imu.getRollPitchYaw()[1], self.__imu.getRollPitchYaw()[2])
        t_base = TransformStamped()
        t_base.header.stamp = Time(seconds=self.__robot.getTime()).to_msg()
        t_base.header.frame_id = 'map'
        t_base.child_frame_id = self.name_value+'/base_link'
        t_base.transform.translation.x = self.__gps.getValues()[0]
        t_base.transform.translation.y = self.__gps.getValues()[1]
        t_base.transform.translation.z = self.__gps.getValues()[2]
        t_base.transform.rotation.x = q[0]
        t_base.transform.rotation.y = q[1]
        t_base.transform.rotation.z = q[2]
        t_base.transform.rotation.w = q[3]
        self.tfbr.sendTransform(t_base)

        forward_speed = self.__target_twist.linear.x
        angular_speed = self.__target_twist.angular.z

        command_motor_left = (forward_speed - angular_speed * HALF_DISTANCE_BETWEEN_WHEELS) / WHEEL_RADIUS
        command_motor_right = (forward_speed + angular_speed * HALF_DISTANCE_BETWEEN_WHEELS) / WHEEL_RADIUS

        self.__left_motor.setVelocity(command_motor_left)
        self.__right_motor.setVelocity(command_motor_right)
