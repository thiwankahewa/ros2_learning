#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class GetPose(Node):
    def __init__(self):
        super().__init__('getPose')
        self.get_logger().info('Get Pose node has been started.')
        self.pose_sub= self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        
    def pose_callback(self, msg):
        self.get_logger().info('Pose: x=%.2f, y=%.2f, theta=%.2f' % (msg.x, msg.y, msg.theta))

def main(args=None):
    rclpy.init(args=args)
    node = GetPose()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()