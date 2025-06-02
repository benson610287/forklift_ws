import rclpy
<<<<<<< HEAD
<<<<<<< HEAD
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
=======
=======
>>>>>>> 2f8df0d86a3d0786f379a4f697a40e86a40618c3
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from pallet_interfaces.msg import Boxinfo

import cv2
import numpy as np

class BoxDetectorNode(Node):
    def __init__(self):
        super().__init__('box_detector_node')

        self.image_sub = self.create_subscription(Image, '/Pallet/BoxImage', self.image_callback, 10)
        self.box_pub = self.create_publisher(Boxinfo, '/Pallet/BoxInfo', 10)
        self.bridge = CvBridge()

        # 假設參考物為 21cm，影像長度為 420 px，計算比例
        self.scale = 21.0 / 420

        # HSV 遮罩範圍（可依實際情況微調）
        self.lower_hsv = np.array([18, 61, 81])
        self.upper_hsv = np.array([30, 213, 233])

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f"CV Bridge Error: {e}")
            return

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)

        # 處理遮罩去雜訊
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        blur = cv2.GaussianBlur(mask, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) < 1000:
                continue

            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                box_pts = approx.reshape(4, 2)
                edge1 = np.linalg.norm(box_pts[0] - box_pts[1])
                edge2 = np.linalg.norm(box_pts[1] - box_pts[2])
                width_px = min(edge1, edge2)
                height_px = max(edge1, edge2)

                width_cm = width_px * self.scale
                height_cm = height_px * self.scale

                # 發佈 box 資訊
                box_msg = Boxinfo()
                box_msg.width = width_cm
                box_msg.length = height_cm
                box_msg.height = 0.0  # 若之後加入高度辨識可更新

                self.box_pub.publish(box_msg)
                self.get_logger().info(f"Box published: {width_cm:.1f}cm x {height_cm:.1f}cm")
                break  # 只處理一個箱子（最明顯的）

        # 顯示除錯視覺（可以註解掉）
        cv2.imshow("Box Detection", frame)
        cv2.imshow("Mask", mask)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = BoxDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()
<<<<<<< HEAD
>>>>>>> taiwen
=======
>>>>>>> 2f8df0d86a3d0786f379a4f697a40e86a40618c3

if __name__ == '__main__':
    main()
