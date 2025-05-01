import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from pallet_interfaces.msg import Boxinfo
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import numpy as np

class BoxDetectorNode(Node):
    def __init__(self):
        super().__init__('box_detector_node')
        self.bridge = CvBridge()

        # --- 1. 訂閱 Topic ---
        self.color_sub = self.create_subscription(
            Image, '/camera/camera/color/image_raw', self.color_callback, 10)
        self.depth_sub = self.create_subscription(
            Image, '/camera/camera/aligned_depth_to_color/image_raw', self.depth_callback, 10)
        self.info_sub = self.create_subscription(
            CameraInfo, '/camera/camera/color/camera_info', self.info_callback, 10)

        # --- 2. YOLO 模型 ---
        self.model = YOLO('work/src/pallet/pallet_main/pallet_main/yolov8n.pt').to('cuda')  # 或換成你自己的 .pt

        # --- 3. 暫存影像 & 內參 ---
        self.color_image = None
        self.depth_image = None
        self.fx = None
        self.fy = None

        # --- 4. 定時器驅動偵測流程 ---
        self.create_timer(0.1, self.detect_loop)  # 10Hz

        # --- 5. Boxinfo Publisher ---
        self.box_pub = self.create_publisher(Boxinfo, '/Pallet/BoxInfo', 10)

    def color_callback(self, msg: Image):
        self.color_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def depth_callback(self, msg: Image):
        # depth 是 16UC1 (mm) 或 32FC1 (m)，pan try both
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        # 如果是 uint16 轉成 float mm，再換成 m
        if img.dtype == np.uint16:
            img = img.astype(np.float32) * 0.001
        self.depth_image = img

    def info_callback(self, msg: CameraInfo):
        if self.fx is None or self.fy is None:
            self.fx = msg.k[0]
            self.fy = msg.k[4]
            self.get_logger().info(f'Loaded intrinsics fx={self.fx:.1f}, fy={self.fy:.1f}')


    def detect_loop(self):
        # 等待所有資料準備好
        if any(x is None for x in (self.color_image, self.depth_image, self.fx, self.fy)):

        # if None in (self.color_image, self.depth_image, self.fx, self.fy):
            return

        # 1. YOLO 偵測
        results = self.model(self.color_image)
        boxes = results[0].boxes.xyxy.cpu().numpy()  # shape=(N,4)

        # 2. 收集 depth + 找最近箱子
        candidates = []
        for x1, y1, x2, y2 in boxes.astype(int):
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            # 防邊界外
            if not (0 <= cy < self.depth_image.shape[0] and 0 <= cx < self.depth_image.shape[1]):
                continue

            # ROI 中位數深度 (m)
            roi = self.depth_image[y1:y2, x1:x2]
            valid = roi[(roi > 0.1) & (roi < 5.0)]  # 0.1~5m 有效範圍
            if valid.size == 0:
                continue
            z = float(np.median(valid))

            candidates.append((z, (x1, y1, x2, y2)))

        if not candidates:
            self.get_logger().info('No valid boxes')
            return

        # 3. 挑最近的那個
        z_nearest, (x1, y1, x2, y2) = min(candidates, key=lambda x: x[0])
        z_nearest*=(39/40)
        # 4. 計算實際長寬 (m)
        w_px = x2 - x1
        h_px = y2 - y1
        w_m = (w_px * z_nearest) / self.fx
        h_m = (h_px * z_nearest) / self.fy

        # 5. 發 Boxinfo
        msg = Boxinfo()
        msg.width = float(w_m * 100)   # 轉 cm
        msg.length = float(h_m * 100)  # 轉 cm
        msg.height = float(z_nearest * 100)  # 轉 cm
        self.box_pub.publish(msg)

        # 6. 視覺化 (除錯用)
        img = self.color_image.copy()
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,0,255), 2)
        label = f'{msg.length:.1f}x{msg.width:.1f}x{msg.height:.1f}cm'
        cv2.putText(img, label, (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        cv2.imshow('Box Detection', img)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = BoxDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
