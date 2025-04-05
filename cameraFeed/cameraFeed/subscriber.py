import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraSubscriber(Node):
    def __init__(self):
        super().__init__('camera_subscriber')
        self.bridgeObject = CvBridge()
        self.subscription = self.create_subscription(
            Image,
            'cameraFeed',
            self.listener_callback,
            20
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('Received image data with height: %d, width: %d' % (msg.height, msg.width))
        open_cv_image = self.bridgeObject.imgmsg_to_cv2(msg)
        cv2.imshow("Camera Feed", open_cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = CameraSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()