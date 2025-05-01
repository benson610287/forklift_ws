import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
from pallet_interfaces.msg import Boxinfo
import numpy as np
import cv2

class RealSenseBoxDetector(Node):
    def __init__(self):
        super().__init__('realsense_box_detector')

        self.bridge = CvBridge()

        self.sub_color = self.create_subscription(Image, '/camera/camera/color/image_raw', self.color_callback, 10)
        self.sub_depth = self.create_subscription(Image, '/camera/camera/aligned_depth_to_color/image_raw', self.depth_callback, 10)

        self.pub_box = self.create_publisher(Boxinfo, '/Pallet/BoxInfo', 10)

        self.latest_color = None
        self.latest_depth = None
        self.depth_scale = 1 # 假設是 mm 轉 m，視你的 RealSense 設定而定

    def color_callback(self, msg):
        self.latest_color = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        self.process_if_ready()

    def depth_callback(self, msg):
        self.latest_depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.process_if_ready()

    def process_if_ready(self):
        if self.latest_color is None or self.latest_depth is None:
            return

        frame = self.latest_color.copy()
        depth_img = self.latest_depth

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower = np.array([18, 61, 81])
        upper = np.array([30, 213, 233])
        mask = cv2.inRange(hsv, lower, upper)

        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        edges = cv2.Canny(mask, 50, 150)

        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.contourArea(cnt) < 1000:
                continue

            approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                pts = approx.reshape(4, 2)

                # 假設四個點是矩形的角落
                p1, p2, p3, p4 = pts

                # 取得角落的深度（Z）
                def get_depth(pt):
                    x, y = int(pt[0]), int(pt[1])
                    return depth_img[y, x] * self.depth_scale  # 單位轉為公尺

                z1 = get_depth(p1)
                z2 = get_depth(p2)
                z3 = get_depth(p3)
                z4 = get_depth(p4)
                z_avg = np.mean([z1, z2, z3, z4])

                # 像素距離轉成真實距離 (approximate, 因為是平面距離)
                def pixel_to_metric(pt1, pt2):
                    dx = pt1[0] - pt2[0]
                    dy = pt1[1] - pt2[1]
                    dist_px = np.sqrt(dx**2 + dy**2)
                    f = 615.0  # 焦距 (要根據相機內參算) ← 可從 CameraInfo 拿
                    dist_m = (dist_px * z_avg) / f
                    return dist_m

                w = pixel_to_metric(p1, p2)
                h = pixel_to_metric(p2, p3)

                msg = Boxinfo()
                msg.width = min(w, h)
                msg.length = max(w, h)
                msg.height = 0.0  # 若有加 top/bottom 可估算高度

                self.pub_box.publish(msg)
                self.get_logger().info(f"📦 Box: {msg.width:.2f}m x {msg.length:.2f}m")
                break

        cv2.imshow("Color", frame)
        cv2.imshow("Mask", mask)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = RealSenseBoxDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
