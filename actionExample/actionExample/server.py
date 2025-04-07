#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle
from custom_interfaces.action import CountUntil
import time

class CustomActionServer(Node):
    def __init__(self):
        super().__init__('action_server')
        self.get_logger().info('Action server started')
        self.countUntilServer = ActionServer(self, CountUntil, 'count_until', self.execute_callback)

    def execute_callback(self, goal_handle:ServerGoalHandle):
        target = goal_handle.request.target_number
        period = goal_handle.request.period
        counter =0
        for i in range(target):
            self.get_logger().info(f'Current value: {counter}')
            counter += 1
            time.sleep(period)

        goal_handle.succeed()
        result = CountUntil.Result()
        result.reached_number = counter
        return result
    
def main(args=None):
    rclpy.init(args=args)
    action_server = CustomActionServer()
    rclpy.spin(action_server)
    action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()