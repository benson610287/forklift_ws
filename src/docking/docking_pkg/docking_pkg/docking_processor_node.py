#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo, PointCloud2
from geometry_msgs.msg import Point, Vector3, Twist
from std_msgs.msg import Header
from sensor_msgs_py import point_cloud2
from cv_bridge import CvBridge
from sklearn.linear_model import RANSACRegressor
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from ultralytics import YOLO
import numpy as np
import cv2
import time
from interface.srv import Maincontroller


class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.last_error = 0.0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return output

    def reset(self):
        self.integral = 0.0
        self.last_error = 0.0


class DockingProcessorNode(Node):
    def __init__(self):
        super().__init__('docking_processor_node')

        self.bridge = CvBridge()
        self.model = YOLO('/home/eating/work/src/docking/docking_pkg/yolov8_models/best.pt')

        self.color_frame = None
        self.depth_frame = None
        self.fx = self.fy = self.cx = self.cy = None

        self.pid_x = PID(1.0, 0.0, 0.1)
        self.pid_z = PID(1.0, 0.0, 0.1)
        self.pid_yaw = PID(1.0, 0.0, 0.1)
        self.target_depth = 0.9

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.create_subscription(Image, '/camera/camera/color/image_raw', self.color_cb, 10)
        self.create_subscription(Image, '/camera/camera/aligned_depth_to_color/image_raw', self.depth_cb, 10)
        self.create_subscription(CameraInfo, '/camera/camera/color/camera_info', self.caminfo_cb, 10)

        self.srv = self.create_service(Maincontroller, 'maincontroller', self.handle_service)
        self.get_logger().info('Docking Processor Node ready.')

    def caminfo_cb(self, msg):
        if self.fx is None:
            self.fx, self.fy = msg.k[0], msg.k[4]
            self.cx, self.cy = msg.k[2], msg.k[5]
            self.get_logger().info(f"Camera intrinsics set: fx={self.fx:.2f}, fy={self.fy:.2f}, cx={self.cx:.2f}, cy={self.cy:.2f}")

    def color_cb(self, msg):
        self.color_frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    def depth_cb(self, msg):
        depth_raw = self.bridge.imgmsg_to_cv2(msg, '16UC1')
        self.depth_frame = depth_raw.astype(np.float32) / 1000.0

    def handle_service(self, request, response):
        if not request.enable:
            response.done = 1
            return response

        self.get_logger().info('Starting docking task...')
        time.sleep(0.5)

        max_iterations = 30
        for i in range(max_iterations):
            if (self.color_frame is None or self.depth_frame is None or self.fx is None):
                self.get_logger().warn('Missing input data.')
                response.done = 2
                return response

            results = self.model(self.color_frame)
            masks = results[0].masks
            if masks is None:
                self.get_logger().warn('No objects detected.')
                continue

            for mask in masks.data:
                mask_np = mask.cpu().numpy().astype(bool)
                points = self.mask_to_points(mask_np)
                if points.shape[0] < 30:
                    continue

                plane_model, inliers = self.fit_plane(points)
                coef, _ = plane_model
                a, b = coef[1], coef[2]
                normal = np.array([a, b, -1.0])
                normal = normal / np.linalg.norm(normal)

                inlier_points = points[inliers]
                center = np.mean(inlier_points, axis=0)

                if self.execute_pid_until_stable(center, normal):
                    response.done = 0
                    return response

        self.get_logger().warn('Docking failed after max attempts.')
        response.done = 4
        return response

    def mask_to_points(self, mask):
        vs, us = np.where(mask)
        if len(us) == 0:
            return np.zeros((0, 3), dtype=np.float32)
        zs = self.depth_frame[vs, us]
        valid = (zs > 0) & ~np.isnan(zs)
        us, vs, zs = us[valid], vs[valid], zs[valid]
        xs = (us - self.cx) * zs / self.fx
        ys = (vs - self.cy) * zs / self.fy
        return np.stack((xs, ys, zs), axis=1)

    def fit_plane(self, points, dist=0.01):
        X, Z = points[:, :2], points[:, 2]
        model = make_pipeline(PolynomialFeatures(1), RANSACRegressor())
        model.fit(X, Z)
        inliers = model.named_steps['ransacregressor'].inlier_mask_
        coef = model.named_steps['ransacregressor'].estimator_.coef_
        intercept = model.named_steps['ransacregressor'].estimator_.intercept_
        return (coef, intercept), inliers

    def execute_pid_until_stable(self, center, normal):
        POSITION_THRESHOLD = 0.01
        ANGLE_THRESHOLD = np.radians(3)
        max_pid_iterations = 20
        dt = 0.1

        for i in range(max_pid_iterations):
            x_error = center[0]
            z_error = self.target_depth - center[2]
            yaw_error = np.arctan2(normal[0], normal[2])

            if normal[2] < 0:
                yaw_error += -np.pi if yaw_error > 0 else np.pi
            if abs(np.degrees(yaw_error)) < 5:
                yaw_error = 0.0

            vx = self.pid_z.update(z_error, dt)
            vy = self.pid_x.update(x_error, dt)
            omega = self.pid_yaw.update(yaw_error, dt)

            twist = Twist()
            twist.linear.x = vx
            twist.linear.y = vy
            twist.angular.z = omega
            self.cmd_pub.publish(twist)

            self.get_logger().info(
                f"[PID {i+1}] Error(x={x_error:.3f}, z={z_error:.3f}, yaw={np.degrees(yaw_error):.2f} deg), "
                f"Twist(x={vx:.2f}, y={vy:.2f}, ω={omega:.2f})"
            )

            if (abs(x_error) < POSITION_THRESHOLD and
                abs(z_error) < POSITION_THRESHOLD and
                abs(yaw_error) < ANGLE_THRESHOLD):
                self.get_logger().info("Docking complete. Errors within threshold.")
                self.cmd_pub.publish(Twist())
                return True

            time.sleep(dt)

        self.cmd_pub.publish(Twist())
        return False


def main(args=None):
    rclpy.init(args=args)
    node = DockingProcessorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
