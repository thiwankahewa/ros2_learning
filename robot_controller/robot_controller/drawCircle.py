#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawCircle(Node):
    def __init__(self):
        super().__init__('drawCircle')
        self.get_logger().info('Draw Circle node has been started.')
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        self.cmd_vel_pub.publish(msg)
        
def main(args=None):
    rclpy.init(args=args)
    node = DrawCircle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

