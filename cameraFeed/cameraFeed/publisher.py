import cv2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.camNO = 0
        self.camera = cv2.VideoCapture(self.camNO)
        self.bridgeObject = CvBridge()
        self.camPubTopic = 'cameraFeed'

        self.publisher = self.create_publisher(Image, self.camPubTopic, 20)
        self.frequency = 0.02

        self.timer = self.create_timer(self.frequency, self.timer_callback)
        self.imageCounter = 0

    def timer_callback(self):
        ret, frame = self.camera.read()
        
        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_CUBIC)
        if ret == True:
            
            # Convert the frame to a ROS Image message
            ros_image = self.bridgeObject.cv2_to_imgmsg(frame)
            self.publisher.publish(ros_image)
            self.imageCounter += 1

def main(args=None):
    rclpy.init(args=args)
    camera_publisher = CameraPublisher()
    rclpy.spin(camera_publisher)
    camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
