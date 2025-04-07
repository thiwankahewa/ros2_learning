#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from custom_interfaces.action import CountUntil


class CustomActionClient(Node):
    def __init__(self):
        super().__init__('action_client')
        self.get_logger().info('Action client started')
        self.countUntilClient = ActionClient(self, CountUntil, 'count_until')

    def send_goal(self, target_number, period):

        self.countUntilClient.wait_for_server()

        goal= CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period

        self.get_logger().info('Sending goal')
        self.countUntilClient.send_goal_async(goal).add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle:ClientGoalHandle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')
        goal_handle.get_result_async().add_done_callback(self.result_callback)
    
    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Final count: {result.reached_number}')
        self.get_logger().info('Goal completed')
        self.destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CustomActionClient()
    node.send_goal(6,1.0)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()