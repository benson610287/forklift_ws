import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from geometry_msgs.msg import Point, Vector3
from visualization_msgs.msg import Marker
from std_msgs.msg import ColorRGBA
import numpy as np
import sensor_msgs_py.point_cloud2 as pc2
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline


class RansacPlaneNode(Node):
    def __init__(self):
        super().__init__('ransac_plane_node')
        
        # 訂閱點雲資料
        self.subscription = self.create_subscription(
            PointCloud2,
            '/processed_points',
            self.pointcloud_callback,
            10
        )

        # 建立 Marker 與平面資訊的 publisher
        self.marker_pub = self.create_publisher(Marker, 'plane_marker', 10)
        self.center_pub = self.create_publisher(Point, 'plane_center', 10)
        self.normal_pub = self.create_publisher(Vector3, 'plane_normal', 10)

        self.get_logger().info('RANSAC Plane Node has been started.')

    def pointcloud_callback(self, msg):
        # 讀取點雲資料
        points = np.array([
            [p[0], p[1], p[2]] for p in pc2.read_points(msg, field_names=("x", "y", "z"), skip_nans=True)
        ])

        if len(points) < 3:
            self.get_logger().warn('點雲中點數不足以擬合平面')
            return

        self.get_logger().info(f"Received point cloud with {len(points)} points")

        # 擬合平面 z = ax + by + c
        X = points[:, :2]  # x, y
        Z = points[:, 2]   # z

        model = make_pipeline(PolynomialFeatures(1), RANSACRegressor())
        model.fit(X, Z)
        inlier_mask = model.named_steps['ransacregressor'].inlier_mask_

        coef = model.named_steps['ransacregressor'].estimator_.coef_
        intercept = model.named_steps['ransacregressor'].estimator_.intercept_

        a = coef[1]
        b = coef[2]
        c = intercept

        self.get_logger().info(f"Plane equation: z = {a:.4f} * x + {b:.4f} * y + {c:.4f}")
        self.get_logger().info(f"Inliers count: {np.sum(inlier_mask)} / {len(points)}")

        # 取得平面中心與法向量
        inlier_points = points[inlier_mask]
        center = np.mean(inlier_points, axis=0)

        normal = np.array([a, b, -1.0])
        normal = normal / np.linalg.norm(normal)

        # ---------- RViz Arrow 可視化法向量 ----------
        arrow_marker = Marker()
        arrow_marker.header = msg.header
        arrow_marker.ns = "plane"
        arrow_marker.id = 0
        arrow_marker.type = Marker.ARROW
        arrow_marker.action = Marker.ADD
        arrow_marker.scale = Vector3(x=0.02, y=0.04, z=0.0)
        arrow_marker.color = ColorRGBA(r=1.0, g=0.0, b=0.0, a=1.0)

        arrow_marker.points.append(Point(
            x=float(center[0]), y=float(center[1]), z=float(center[2])
        ))

        arrow_length = 0.2
        end = center + normal * arrow_length
        arrow_marker.points.append(Point(
            x=float(end[0]), y=float(end[1]), z=float(end[2])
        ))

        self.marker_pub.publish(arrow_marker)

        # ---------- RViz Sphere 可視化中心 ----------
        sphere_marker = Marker()
        sphere_marker.header = msg.header
        sphere_marker.ns = "plane_center"
        sphere_marker.id = 1
        sphere_marker.type = Marker.SPHERE
        sphere_marker.action = Marker.ADD
        sphere_marker.pose.position = Point(
            x=float(center[0]), y=float(center[1]), z=float(center[2])
        )
        sphere_marker.scale = Vector3(x=0.05, y=0.05, z=0.05)
        sphere_marker.color = ColorRGBA(r=0.0, g=1.0, b=0.0, a=1.0)

        self.marker_pub.publish(sphere_marker)

        # ---------- 發布中心點與法向量 (Point / Vector3) ----------
        center_msg = Point(
            x=float(center[0]), y=float(center[1]), z=float(center[2])
        )
        self.center_pub.publish(center_msg)

        normal_msg = Vector3(
            x=float(normal[0]), y=float(normal[1]), z=float(normal[2])
        )
        self.normal_pub.publish(normal_msg)

        # ---------- 記錄到 log ----------
        self.get_logger().info(f"Plane center: ({center[0]:.2f}, {center[1]:.2f}, {center[2]:.2f})")
        self.get_logger().info(f"Plane normal: ({normal[0]:.4f}, {normal[1]:.4f}, {normal[2]:.4f})")


def main(args=None):
    rclpy.init(args=args)
    node = RansacPlaneNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
