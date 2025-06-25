#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2, CameraInfo
from std_msgs.msg import Header
from sensor_msgs_py import point_cloud2
from cv_bridge import CvBridge
import numpy as np
import cv2
import open3d as o3d
from ultralytics import YOLO


class YoloDepthProcessor(Node):
    # --------------------------------------------------
    def __init__(self):
        super().__init__('yolo_depth_processor')

        # === 0. 變數初始化 ===
        self.bridge = CvBridge()
        self.model = YOLO('/home/eating/work/src/docking/docking_pkg/yolov8_models/best.pt')

        self.color_frame = None
        self.depth_frame = None
        self.fx = self.fy = self.cx = self.cy = None   # 待 CameraInfo 設定

        # === 1. ROS 訂閱 ===
        self.create_subscription(Image,      '/camera/camera/color/image_raw',
                                 self.color_cb,   10)
        self.create_subscription(Image,      '/camera/camera/aligned_depth_to_color/image_raw',
                                 self.depth_cb,   10)
        self.create_subscription(CameraInfo, '/camera/camera/color/camera_info',
                                 self.caminfo_cb, 10)

        # === 2. 點雲發布 ===
        self.pc_pub = self.create_publisher(PointCloud2, '/processed_points', 10)
        self.get_logger().info('YoloDepthProcessor node up.')

    # --------------------------------------------------
    # CameraInfo → 讀取內參
    def caminfo_cb(self, msg: CameraInfo):
        if self.fx is None:         # 只設定一次
            self.fx = msg.k[0]
            self.fy = msg.k[4]
            self.cx = msg.k[2]
            self.cy = msg.k[5]
            self.get_logger().info(
                f'Camera intrinsics set | fx={self.fx:.2f}, fy={self.fy:.2f}, '
                f'cx={self.cx:.2f}, cy={self.cy:.2f}')

    # 彩色
    def color_cb(self, msg: Image):
        self.color_frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        self.process()

    # 對齊深度（32FC1 → 公尺）
    def depth_cb(self, msg: Image):
        # 1. 正確讀取為 uint16
        depth_raw = self.bridge.imgmsg_to_cv2(msg, '16UC1')

        # 2. 轉為公尺（float32）
        self.depth_frame = depth_raw.astype(np.float32) / 1000.0

        
        # 添加深度圖像診斷
        depth_min = np.nanmin(self.depth_frame)
        depth_max = np.nanmax(self.depth_frame)
        num_valid = np.sum((self.depth_frame > 0) & ~np.isnan(self.depth_frame))
        
        self.get_logger().info(
            f"Depth range: {depth_min:.2f}-{depth_max:.2f}m | "
            f"Valid pixels: {num_valid}/{self.depth_frame.size}"
        )
        

    # --------------------------------------------------
    def process(self):
        if (self.color_frame is None or
            self.depth_frame is None or
            self.fx is None):
            self.get_logger().debug("Waiting for all data to be available...")
            return  # 等待資料齊全

        results = self.model(self.color_frame)
        masks = results[0].masks
        if masks is None:
            self.get_logger().debug('No masks detected')
            return

        self.get_logger().info(f'Detected {len(masks.data)} masks')

        for idx, mask in enumerate(masks.data):
            mask_np = mask.cpu().numpy().astype(bool)
            points = self.mask_to_points(mask_np)

            # 添加檢查：確保points不是None且有正確形狀
            if points is None or points.shape[0] == 0:
                self.get_logger().warning(f'Mask {idx}: No valid points after processing')
                continue

            self.get_logger().info(f'Mask {idx}: {points.shape[0]} valid points')

            if points.shape[0] < 30:
                self.get_logger().warning(f'Mask {idx} too few points, skip')
                continue

            try:
                plane, inliers = self.fit_plane(points)
                inlier_pts = points[inliers]
                self.get_logger().info(
                    f'Mask {idx}: plane {np.round(plane,3)}, inliers={inlier_pts.shape[0]}')
                self.publish_cloud(inlier_pts)
            except Exception as e:
                self.get_logger().error(f'Error processing mask {idx}: {str(e)}')

    # ---------- 工具 ----------
    def mask_to_points(self, mask):
        vs, us = np.where(mask)
        # 添加邊界檢查
        valid = (us >= 0) & (us < self.depth_frame.shape[1]) & \
                (vs >= 0) & (vs < self.depth_frame.shape[0])
        us, vs = us[valid], vs[valid]

        if len(vs) == 0 or len(us) == 0:
            self.get_logger().warn("Empty mask received!")
            return np.zeros((0,3), dtype=np.float32)
        
        zs = self.depth_frame[vs, us]
        self.get_logger().info(f"Pre-filter points: {len(zs)}")
        
        good = (zs > 0) & ~np.isnan(zs)

        us, vs, zs = us[good], vs[good], zs[good]
        self.get_logger().info(f"Post-filter points: {len(zs)}")
    
        # 添加檢查：如果過濾後沒有點，返回空陣列
        if len(zs) == 0:
            return np.zeros((0,3), dtype=np.float32)
        
        # 計算3D座標
        xs = (us - self.cx) * zs / self.fx
        ys = (vs - self.cy) * zs / self.fy
        
        # 返回3D點雲
        return np.stack((xs, ys, zs), axis=1).astype(np.float32)
    

    # ... rest of the function ...

    def fit_plane(self, points, dist=0.01):
        pcd = o3d.geometry.PointCloud(o3d.utility.Vector3dVector(points))
        return pcd.segment_plane(dist, 3, 1000)  # plane_model, inlier_idx

    def publish_cloud(self, points):
        try:
            if points.size == 0:
                self.get_logger().warn("Attempted to publish empty point cloud")
                return
        
            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            header.frame_id = 'camera_color_optical_frame'
        
            self.get_logger().info(f"Publishing {len(points)} points")
        
            msg = point_cloud2.create_cloud_xyz32(header, points.tolist())
            self.pc_pub.publish(msg)
            self.get_logger().info("Point cloud published successfully")
        except Exception as e:
            self.get_logger().error(f"Error publishing point cloud: {str(e)}")


# --------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = YoloDepthProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
