import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os

from ament_index_python.packages import get_package_share_directory
import os

class ImagePublisherNode(Node):
    def __init__(self):
        super().__init__('image_publisher_node')

        self.publisher = self.create_publisher(Image, 'image', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.bridge = CvBridge()

        # 使用 ROS 套件資源方式取得圖片路徑
        pkg_share = get_package_share_directory('pallet_monitoring')
        image_path = os.path.join(pkg_share, 'img', 'test_image.jpg')
        self.get_logger().info(f'🔍 嘗試讀取圖片：{image_path}')
        self.image = cv2.imread(image_path)

        if self.image is None:
            self.get_logger().error(f"❌ 無法讀取圖片：{image_path}")
        else:
            self.get_logger().info(f"✅ 成功載入圖片：{image_path}")


    def timer_callback(self):
        if self.image is not None:
            msg = self.bridge.cv2_to_imgmsg(self.image, encoding='bgr8')
            self.publisher.publish(msg)
            self.get_logger().info('📤 發佈圖片到 /image')

def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
