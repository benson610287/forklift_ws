import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from pallet_interfaces.msg import Boxinfo
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
from ultralytics import YOLO
import cv2
import numpy as np

class BoxDetectorNode(Node):
    def __init__(self):
        super().__init__('box_detector_node')
        self.bridge = CvBridge()
        self.pallet_mode=0
        # --- 1. 訂閱 Topic ---
        self.color_sub = self.create_subscription(
            Image, '/camera/Armcamera/color/image_raw', self.color_callback, 10)
        self.depth_sub = self.create_subscription(
            Image, '/camera/Armcamera/aligned_depth_to_color/image_raw', self.depth_callback, 10)
        self.info_sub = self.create_subscription(
            CameraInfo, '/camera/Armcamera/color/camera_info', self.info_callback, 10)
        # --- 5. Boxinfo Publisher ---
        self.box_pub = self.create_publisher(Int64, '/Pallet/boxtype', 10)
        self.box_pubb = self.create_publisher(Int64, '/Pallet/SingBoxInfo', 10)
        self.pose_pub = self.create_publisher(Twist, '/Pallet/virtualstartpose', 10)
        # --- 2. YOLO 模型 ---
        self.model = YOLO('src/pallet/pallet_main/pallet_main/best.pt').to('cuda')  

        # --- 3. 暫存影像 & 內參 ---
        self.color_image = None
        self.depth_image = None
        self.fx = None
        self.fy = None

        # --- 4. 定時器驅動偵測流程 ---
        self.get_yolo_sub=self.create_subscription(Int64,'Pallet/yolo_cmd',self.detect_loop,10)
        # self.create_timer(0.1, self.detect_loop_test)  # 10Hz



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

    # def detect_loop_test(self):
    #     boxtype=0
    #     # 等待所有資料準備好
    #     if any(x is None for x in (self.color_image, self.depth_image, self.fx, self.fy)):

    #     # if None in (self.color_image, self.depth_image, self.fx, self.fy):
    #         return

    #     # 1. YOLO 偵測
    #     results = self.model(self.color_image)
    #     # boxes = results[0].boxes.xyxy.cpu().numpy()  # shape=(N,4)
    #     boxes = results[0].obb.xywhr.cpu().numpy()

    #     candidates = []
    #     for xc, yc, w, h, angle in boxes:
    #         rect = ((xc, yc), (w, h), np.degrees(angle))
    #         box = cv2.boxPoints(rect).astype(int)

    #         x_min = np.clip(np.min(box[:, 0]), 0, self.depth_image.shape[1] - 1)
    #         x_max = np.clip(np.max(box[:, 0]), 0, self.depth_image.shape[1] - 1)
    #         y_min = np.clip(np.min(box[:, 1]), 0, self.depth_image.shape[0] - 1)
    #         y_max = np.clip(np.max(box[:, 1]), 0, self.depth_image.shape[0] - 1)

    #         # ROI 中位數深度 (m)
    #         roi = self.depth_image[y_min:y_max, x_min:x_max]
    #         valid = roi[(roi > 0.1) & (roi < 5.0)]
    #         if valid.size == 0:
    #             continue

    #         z = float(np.median(valid))
    #         candidates.append((z, box))  # 你也可以保留 boxPoints 結果


    #     # 3. 挑最近的那個
    #     z_nearest, box_nearest = min(candidates, key=lambda x: x[0])
    #     z_nearest *= (39 / 40)  # 校正

    #     # 4. 計算實際長寬 (m) —— 使用 box 四點計算像素長寬
    #     # box_nearest 是 shape (4,2)，每兩個相鄰點為一條邊
    #     edge_lengths = [np.linalg.norm(box_nearest[i] - box_nearest[(i + 1) % 4]) for i in range(4)]
    #     w_px = max(edge_lengths)
    #     h_px = min(edge_lengths)

    #     # 透過相機內參換算成實際尺寸
    #     w_m = (w_px * z_nearest) / self.fx
    #     h_m = (h_px * z_nearest) / self.fy

    #     # 5. 發 Boxinfo
    #     inner_msg = Int64()
    #     width = float(w_m * 100)   # 轉 cm
    #     length = float(h_m * 100)  # 轉 cm
    #     height = float(z_nearest * 100)  # 轉 cm
    #     if 22.5>=width>=17.5 and 32.5>=length>=27.5:
    #         inner_msg.data=2
    #     else:
    #         inner_msg.data=-1
    #         pass
    #     if boxtype==0:
            
    #         self.box_pub.publish(inner_msg)
    #     else:
    #         pass
    #         # self.box_pubb.publish(msg)

    #     # 6. 視覺化 (除錯用)
    #     img = self.color_image.copy()

    #     # 繪製旋轉框
    #     cv2.polylines(img, [box_nearest], isClosed=True, color=(0, 0, 255), thickness=2)

    #     # 顯示尺寸資訊（單位換算成 cm）
    #     label = f'{w_m*100:.1f}x{h_m*100:.1f}cm'
    #     print(label)
    #     text_origin = tuple(box_nearest[0])  # 以第 1 個點為起始
    #     cv2.putText(img, label, text_origin,
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    #     cv2.imshow('Box Detection', img)
    #     cv2.waitKey(1)

    def detect_loop(self,msg):
        
        # 等待所有資料準備好
        if any(x is None for x in (self.color_image, self.depth_image, self.fx, self.fy)):

        # if None in (self.color_image, self.depth_image, self.fx, self.fy):
            return

        # 1. YOLO 偵測
        results = self.model(self.color_image)
        # boxes = results[0].boxes.xyxy.cpu().numpy()  # shape=(N,4)
        boxes = results[0].obb.xywhr.cpu().numpy()
        scores = results[0].obb.conf.cpu().numpy()
        candidates = []
        print(len(boxes))
        if len(boxes)==0:
            self.get_logger().error('no box detected')
            return
        id=0
        for (xc, yc, w, h, angle), conf in zip(boxes, scores):
            print("ID=",id,"w=",w,"h=",h,"angle=",angle,"conf=",conf)
            id+=1
            # angle=1.57
            if conf>0.45:
                rect = ((xc, yc), (w, h), np.degrees(angle))
                box = cv2.boxPoints(rect).astype(int)

                x_min = np.clip(np.min(box[:, 0]), 0, self.depth_image.shape[1] - 1)
                x_max = np.clip(np.max(box[:, 0]), 0, self.depth_image.shape[1] - 1)
                y_min = np.clip(np.min(box[:, 1]), 0, self.depth_image.shape[0] - 1)
                y_max = np.clip(np.max(box[:, 1]), 0, self.depth_image.shape[0] - 1)

                # ROI 中位數深度 (m)
                roi = self.depth_image[y_min:y_max, x_min:x_max]
                valid = roi[(roi > 0.1) & (roi < 5.0)]
                if valid.size == 0:
                    continue

                z = float(np.median(valid))
                candidates.append((z, box))  # 你也可以保留 boxPoints 結果


        # 3. 挑最近的那個
        z_nearest, box_nearest = min(candidates, key=lambda x: x[0])
        z_nearest *= (7.0 / 8.0*7.1/7.4)  # 校正
        # z_nearest = z_nearest-0.06 # 校正
        # --- Publish Center + Angle ---
        pose_msg = Twist()

        # 中心點像素位置轉實際距離
        center_x = np.mean(box_nearest[:, 0])
        center_y = np.mean(box_nearest[:, 1])

        # 將 pixel 坐標轉換成相機座標系下的 (x, y, z)
        x_m = ((center_x - self.depth_image.shape[1] / 2) * z_nearest) / self.fx
        y_m = ((center_y - self.depth_image.shape[0] / 2) * z_nearest) / self.fy

        pose_msg.linear.x = float(x_m*1000)
        pose_msg.linear.y = float(y_m*1000)
        # pose_msg.linear.z = float(z_nearest*1000)  # depth

        # 計算角度（角度轉換成 -pi ~ pi 區間）
        angle_deg = np.degrees(angle)
        angle_rad = float(angle)
        pose_msg.angular.z = angle_rad

        
        self.get_logger().info(f'Pose published: x={x_m:.2f}, y={y_m:.2f}, z={z_nearest:.2f}, angle(deg)={angle_deg:.1f}')

        # 4. 計算實際長寬 (m) —— 使用 box 四點計算像素長寬
        # box_nearest 是 shape (4,2)，每兩個相鄰點為一條邊
        edge_lengths = [np.linalg.norm(box_nearest[i] - box_nearest[(i + 1) % 4]) for i in range(4)]
        w_px = min(edge_lengths)
        h_px = max(edge_lengths)

        # 透過相機內參換算成實際尺寸
        w_m = (w_px * z_nearest) / self.fx
        h_m = (h_px * z_nearest) / self.fy
        # 5. 發 Boxinfo
        inner_msg = Int64()
        width = float(w_m * 100)   # 轉 cm
        length = float(h_m * 100)  # 轉 cm
        height = float(z_nearest * 100)  # 轉 cm
        self.get_logger().info(f'Box dimensions (cm): width={width}, length={length}, height={height}')
        if 27.5>=width>=22.5 and 32.5>=length>=27.5:
            inner_msg.data=2 #mid
            pose_msg.linear.z = float(150.0)
            self.pose_pub.publish(pose_msg)
        elif 32.5>=width>=27.5 and 42.5>=length>=37.5:
            inner_msg.data=1 #big
            pose_msg.linear.z = float(200.0)
            self.pose_pub.publish(pose_msg)
        elif 13.5>=width>=8.5 and 23>=length>=18:
            inner_msg.data=3 #small
            pose_msg.linear.z = float(140.0)
            self.pose_pub.publish(pose_msg)
        else:
            self.get_logger().error('box type error')
            # 6. 視覺化 (除錯用)
            img = self.color_image.copy()

            # 繪製旋轉框
            cv2.polylines(img, [box_nearest], isClosed=True, color=(0, 0, 255), thickness=2)

            # 顯示尺寸資訊（單位換算成 cm）
            label = f'{w_m*100:.1f}x{h_m*100:.1f}cm'
            print(label)
            text_origin = tuple(box_nearest[0])  # 以第 1 個點為起始
            cv2.putText(img, label, text_origin,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # cv2.imshow('Box Detection', img)
            cv2.imwrite('box.jpg',img)
            return


            
        if msg.data==0:
            self.get_logger().info(f'box_pub={inner_msg.data}')
            # print("box_pub=",inner_msg.data)
            self.box_pub.publish(inner_msg)
        elif msg.data==1:
            self.get_logger().info(f'box_pubb={inner_msg.data}')
            # print("box_pubb=",inner_msg.data)
            self.box_pubb.publish(inner_msg)
            # self.box_pubb.publish(msg)

        # 6. 視覺化 (除錯用)
        img = self.color_image.copy()

        # 繪製旋轉框
        cv2.polylines(img, [box_nearest], isClosed=True, color=(0, 0, 255), thickness=2)

        # 顯示尺寸資訊（單位換算成 cm）
        label = f'{w_m*100:.1f}x{h_m*100:.1f}cm'
        print(label)
        text_origin = tuple(box_nearest[0])  # 以第 1 個點為起始
        cv2.putText(img, label, text_origin,
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # cv2.imshow('Box Detection', img)
        cv2.imwrite('box.jpg',img)


def main(args=None):
    rclpy.init(args=args)
    node = BoxDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
