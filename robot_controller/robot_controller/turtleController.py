#/!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from turtlesim.srv import SetPen

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtleController')
        self.previousX = 0
        self.get_logger().info('Turtle Controller node has been started.')
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

    def pose_callback(self, msg):
        cmd = Twist()
        if msg.x > 9.0 or msg.x < 2.0 or msg.y > 9.0 or msg.y < 2.0:
            cmd.linear.x = 2.0
            cmd.angular.z = 1.0 
        else:
            cmd.linear.x = 5.0
            cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

        if msg.x > 5.5 and self.previousX <= 5.5:
            self.previousX = msg.x
            self.call_set_pen_service(255, 0, 0, 2, 0)
        elif msg.x <= 5.5 and self.previousX > 5.5:
            self.previousX = msg.x
            self.call_set_pen_service(0, 255, 0, 2, 0)

    def call_set_pen_service(self,r,g,b,width,off):                                 #coding for a service call
        client  = self.create_client(SetPen, '/turtle1/set_pen')                    #creating a client for the SetPen service
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')      #waiting for the service to be available
        
        request = SetPen.Request()                                                  #creating a request object
        request.r = r
        request.g = g
        request.b = b
        request.width = width
        request.off = off
 
        future = client.call_async(request)                                      #calling the service asynchronously
        future.add_done_callback(self.set_pen_callback)                          #adding a callback to handle the response

    def set_pen_callback(self, future):                                           #callback function to handle the response
        try:
            response = future.result()
        except Exception as e:
            self.get_logger().info('Service call failed %r' % (e,))
        
def main(args=None):
    rclpy.init(args=args)
    node = TurtleController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()