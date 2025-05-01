
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('handcamera')
        self.publisher_ = self.create_publisher(Image, '/Pallet/BoxImage', 10)
        self.timer_ = self.create_timer(0.01, self.publish_image)
        self.bridge_ = CvBridge()
        self.cap = cv2.VideoCapture(25) 
        self.bridge = CvBridge()

        if not self.cap.isOpened():
            self.get_logger().error('Unable to open the camera.')
            raise RuntimeError('Unable to open the camera.')
    def publish_image(self):
        ret, frame = self.cap.read()
        if ret:
            try:
                ros_image_msg = self.bridge.cv2_to_imgmsg(frame, encoding='bgr8')
                self.publisher_.publish(ros_image_msg)
                self.get_logger().info('Image published to camera_image topic')
            except Exception as e:
                self.get_logger().error(f'Error converting and publishing image: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

