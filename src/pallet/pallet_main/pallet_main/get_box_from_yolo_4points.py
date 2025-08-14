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

        # --- 訂閱相機影像與內參 ---
        self.color_sub = self.create_subscription(
            Image, '/camera/camera/color/image_raw', self.color_callback, 10)
        self.depth_sub = self.create_subscription(
            Image, '/camera/camera/aligned_depth_to_color/image_raw', self.depth_callback, 10)
        self.info_sub = self.create_subscription(
            CameraInfo, '/camera/camera/color/camera_info', self.info_callback, 10)

        # --- 載入 YOLO 模型 ---
        self.model = YOLO('work/src/pallet/pallet_main/pallet_main/yolov8n.pt')

        # --- 資料儲存 ---
        self.color_image = None
        self.depth_image = None
        self.fx = None
        self.fy = None

        # --- Timer: 10Hz 執行辨識 ---
        self.create_timer(0.1, self.detect_loop)

        # --- Boxinfo 發布者 ---
        self.box_pub = self.create_publisher(Boxinfo, '/Pallet/BoxInfo', 10)

    def color_callback(self, msg: Image):
        self.color_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def depth_callback(self, msg: Image):
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        if img.dtype == np.uint16:
            img = img.astype(np.float32) * 0.001  # 轉成公尺
        self.depth_image = img

    def info_callback(self, msg: CameraInfo):
        self.fx = msg.k[0]
        self.fy = msg.k[4]
        self.get_logger().info(f'Loaded intrinsics fx={self.fx:.1f}, fy={self.fy:.1f}')

    def compute_size_from_corners(self, x1, y1, x2, y2):
        # 四個角落的像素位置
        corners = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
        points_3d = []

        for (x, y) in corners:
            if not (0 <= y < self.depth_image.shape[0] and 0 <= x < self.depth_image.shape[1]):
                continue
            z = float(self.depth_image[y, x])
            if z == 0.0:
                continue
            X = (x - self.color_image.shape[1] / 2) * z / self.fx
            Y = (y - self.color_image.shape[0] / 2) * z / self.fy
            points_3d.append(np.array([X, Y, z]))

        if len(points_3d) < 4:
            self.get_logger().warn("Not enough valid depth points for corners.")
            return None, None

        width1 = np.linalg.norm(points_3d[0] - points_3d[1])
        width2 = np.linalg.norm(points_3d[3] - points_3d[2])
        length1 = np.linalg.norm(points_3d[0] - points_3d[3])
        length2 = np.linalg.norm(points_3d[1] - points_3d[2])

        width = (width1 + width2) / 2
        length = (length1 + length2) / 2
        return width, length

    def detect_loop(self):
        if any(x is None for x in (self.color_image, self.depth_image, self.fx, self.fy)):
            return

        results = self.model(self.color_image)
        boxes = results[0].boxes.xyxy.cpu().numpy()

        candidates = []
        for x1, y1, x2, y2 in boxes.astype(int):
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            if not (0 <= cy < self.depth_image.shape[0] and 0 <= cx < self.depth_image.shape[1]):
                continue

            roi = self.depth_image[y1:y2, x1:x2]
            valid = roi[(roi > 0.1) & (roi < 5.0)]
            if valid.size == 0:
                continue
            z = float(np.median(valid))
            candidates.append((z, (x1, y1, x2, y2)))

        if not candidates:
            self.get_logger().info('No valid boxes')
            return

        z_nearest, (x1, y1, x2, y2) = min(candidates, key=lambda x: x[0])

        # ✅ 改用四角深度計算實際長寬
        w_m, h_m = self.compute_size_from_corners(x1, y1, x2, y2)
        if w_m is None or h_m is None:
            return

        # ✅ 發布 Boxinfo（單位 cm）
        msg = Boxinfo()
        msg.width = float(w_m * 100)
        msg.length = float(h_m * 100)
        msg.height = float(z_nearest * 100)
        self.box_pub.publish(msg)

        # ✅ 視覺化
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
