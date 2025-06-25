import rclpy
import math
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from pallet_interfaces.msg import Boxinfo
import math
import random
class TurtlePControl(Node):
    def __init__(self):
        super().__init__('GetBox')

        # 訂閱烏龜的位置信息
        self.pose_subscriber = self.create_subscription(Image, '/Pallet/BoxImage', self.img_callback, 10)
        self.cv_bridge=CvBridge()
        # 發布速度指令
        self.box=Boxinfo()
        self.velocity_publisher = self.create_publisher(Boxinfo, '/Pallet/BoxInfo', 10)

        self.timer = self.create_timer(1/30, self.control_loop)  # 100ms 週期執行

    def img_callback(self, msg):
        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error converting image: {e}')
            return

        cv2.imshow('Image', cv_image)
        key = cv2.waitKey(1)

        # if key == ord('q') and not self.recording:
        #     self.start_recording(cv_image.shape[1], cv_image.shape[0])  # 寬度和高度
        # elif key == ord('q') and self.recording:
        #     self.stop_recording()

        # if self.recording:
        #     self.video_writer.write(cv_image)

    def control_loop(self):
        pass
        self.box.length=10.5
        self.box.width=12.1
        self.box.height=8.2
        self.velocity_publisher.publish(self.box)
        # self.velocity_publisher.publish(cmd_vel)
            # 發佈速度：依照 P 控制所計算的線速度


            # 顯示當前狀態
        # self.get_logger().info(f'距離目標: {cmd_vel:.2f}, 設定線速度: {cmd_vel:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtlePControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
