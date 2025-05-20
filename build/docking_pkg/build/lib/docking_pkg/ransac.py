import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point, Vector3
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

class RansacPlaneNode(Node):
    def __init__(self):
        super().__init__('ransac_plane_node')
        self.subscription = self.create_subscription(
            PointCloud2,
            '/processed_points',
            self.pointcloud_callback,
            10
        )
        self.get_logger().info('RANSAC Plane Node has been started.')

    def pointcloud_callback(self, msg):
        # 讀取點雲
        points = np.array([
            [p[0], p[1], p[2]] for p in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
        ])

        if len(points) < 3:
            self.get_logger().warn('點雲中點數不足以擬合平面')
            return

        self.get_logger().info(f"Received point cloud with {len(points)} points")

        # 分割 x, y, z
        X = points[:, :2]  # x, y
        Z = points[:, 2]   # z

        # RANSAC 擬合 z = a * x + b * y + c
        model = make_pipeline(PolynomialFeatures(1), RANSACRegressor())
        model.fit(X, Z)
        inlier_mask = model.named_steps['ransacregressor'].inlier_mask_

        # 提取平面係數
        coef = model.named_steps['ransacregressor'].estimator_.coef_
        intercept = model.named_steps['ransacregressor'].estimator_.intercept_

        a = coef[1]  # x
        b = coef[2]  # y
        c = intercept

        self.get_logger().info(f"Plane equation: z = {a:.4f} * x + {b:.4f} * y + {c:.4f}")
        self.get_logger().info(f"Inliers count: {np.sum(inlier_mask)} / {len(points)}")

        # --- 取得中心點與法向量 ---
        inlier_points = points[inlier_mask]
        center = np.mean(inlier_points, axis=0)

        normal = np.array([a, b, -1.0])
        normal = normal / np.linalg.norm(normal)

        self.get_logger().info(f"Plane center: ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})")
        self.get_logger().info(f"Plane normal: ({normal[0]:.4f}, {normal[1]:.4f}, {normal[2]:.4f})")

        # (可選) 接下來你可以發佈這些資訊給其他節點使用或做成 Marker

def main(args=None):
    rclpy.init(args=args)
    node = RansacPlaneNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
