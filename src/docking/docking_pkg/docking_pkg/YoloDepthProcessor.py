import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, PointCloud2
from sensor_msgs.msg import PointField
from sensor_msgs_py import point_cloud2

from cv_bridge import CvBridge
import numpy as np
import cv2
from ultralytics import YOLO
import open3d as o3d

class YoloDepthProcessor(Node):
    def __init__(self):
        super().__init__('yolo_depth_processor')
        self.bridge = CvBridge()
        self.model = YOLO('/home/eating/work/src/docking/docking_pkg/yolov8_models/last.pt')

        self.create_subscription(Image, '/camera/camera/color/image_raw', self.image_callback, 10)
        self.create_subscription(Image, '/camera/camera/depth/image_rect_raw', self.depth_callback, 10)

        self.pc_publisher = self.create_publisher(PointCloud2, 'processed_points', 10)

        self.color_frame = None
        self.depth_frame = None

        # 攝影機內參（請換成你的實際值）
        self.fx = 525.0
        self.fy = 525.0
        self.cx = 319.5
        self.cy = 239.5

    def publish_pointcloud(self, points):
        if points.shape[0] == 0:
            return
        header = self.get_clock().now().to_msg()
        pc_msg = point_cloud2.create_cloud_xyz32(
            header=PointCloud2().header,
            points=points.tolist()
        )
        pc_msg.header.stamp = self.get_clock().now().to_msg()
        pc_msg.header.frame_id = 'camera_link'  # 替換成你的相機 TF frame
        self.pc_publisher.publish(pc_msg)

    def image_callback(self, msg):
        self.color_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.get_logger().info(f'Received color frame: {self.color_frame.shape}')
        self.process()

    def depth_callback(self, msg):
        self.depth_frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.get_logger().info(f'Received depth frame: {self.depth_frame.shape}')

    def process(self):
        if self.color_frame is None or self.depth_frame is None:
            return

        try:
            results = self.model(self.color_frame)
            masks = results[0].masks

            if masks is not None:
                self.get_logger().info(f'Detected {len(masks.data)} masks')

                for idx, mask in enumerate(masks.data):
                    mask_np = mask.cpu().numpy().astype(bool)

                    points = self.depth_to_points(mask_np, self.depth_frame)

                    if points.shape[0] < 3:
                        self.get_logger().warning(f'Mask {idx} has too few points ({points.shape[0]}), skipping')
                        continue

                    plane_model, inliers = self.fit_plane(points)
                    self.get_logger().info(f'Mask {idx}: Plane {plane_model}, inliers: {len(inliers)}')

                    self.publish_pointcloud(points)

        except Exception as e:
            self.get_logger().error(f'Error in process(): {e}')

    def depth_to_points(self, mask, depth_frame):
        indices = np.argwhere(mask)
        points = []
        for (v, u) in indices:
            z = depth_frame[v, u]
            if z == 0 or np.isnan(z):
                continue
            x = (u - self.cx) * z / self.fx
            y = (v - self.cy) * z / self.fy
            points.append([x, y, z])
        points_np = np.array(points, dtype=np.float32)
        self.get_logger().info(f'Generated {points_np.shape[0]} 3D points from mask')
        return points_np

    def fit_plane(self, points):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)
        plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3, num_iterations=1000)
        return plane_model, inliers

def main(args=None):
    rclpy.init(args=args)
    node = YoloDepthProcessor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down by KeyboardInterrupt')
    finally:
        node.destroy_node()
        rclpy.shutdown()
