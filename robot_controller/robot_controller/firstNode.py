
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class FirstNode(Node):
    def __init__(self):
        super().__init__('first_node')
        self.get_logger().info('First node has been started.')
        self.counter = 0
        self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info('Hello '+str(self.counter))
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = FirstNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    






