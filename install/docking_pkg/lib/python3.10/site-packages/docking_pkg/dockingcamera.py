import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import pyrealsense2 as rs
import numpy as np

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('dockingcamera')
        self.bridge = CvBridge()

        # RealSense pipeline 初始化
        self.pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        self.pipeline.start(config)

        # 建立 ROS 發布器
        self.color_pub = self.create_publisher(Image, '/Docking/PalletImage', 10)
        self.depth_pub = self.create_publisher(Image, '/Docking/PalletDepth', 10)

        self.timer = self.create_timer(0.03, self.publish_images)

    def publish_images(self):
        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        depth_frame = frames.get_depth_frame()

        if not color_frame or not depth_frame:
            self.get_logger().warning('Frame not received')
            return

        # 轉成 numpy
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())

        # 轉 ROS 訊息
        color_msg = self.bridge.cv2_to_imgmsg(color_image, encoding='bgr8')
        depth_msg = self.bridge.cv2_to_imgmsg(depth_image, encoding='16UC1')  # 注意是 16 位元單通道

        self.color_pub.publish(color_msg)
        self.depth_pub.publish(depth_msg)

        self.get_logger().info('Published color and depth images')

def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher()
    rclpy.spin(node)
    node.pipeline.stop()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
