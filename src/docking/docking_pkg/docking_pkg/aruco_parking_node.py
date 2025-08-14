import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np
import math


class ArucoParkingNode(Node):
    def __init__(self):
        super().__init__('aruco_align_node')

        self.bridge = CvBridge()
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.create_subscription(Image, '/camera/camera/color/image_raw', self.image_callback, 10)
        self.create_subscription(CameraInfo, '/camera/camera/color/camera_info', self.camera_info_callback, 10)

        self.K = None
        self.D = None
        self.marker_length = 0.1  # 10cm
        self.target_distance = 1.4

        self.linear_k = 0.3
        self.lateral_k = -0.1
        self.angular_k = -0.0008

        self.success_count = 0

        self.ARUCO_DICT = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.ARUCO_DETECTOR = cv2.aruco.ArucoDetector(self.ARUCO_DICT, cv2.aruco.DetectorParameters())

        self.get_logger().info('Aruco Align Node ready.')

    def camera_info_callback(self, msg):
        if self.K is None:
            self.K = np.array(msg.k, dtype=np.float64).reshape(3, 3)
            self.D = np.array(msg.d, dtype=np.float64)
            self.get_logger().info('Camera parameters received.')

    def image_callback(self, msg):
        if self.K is None:
            return

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, _ = self.ARUCO_DETECTOR.detectMarkers(gray)
        cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        # 顯示畫面
        cv2.imshow('Aruco Markers', frame)
        cv2.waitKey(1)

        if ids is None or len(ids) == 0:
            # 看不到任何 ArUco marker 時，送出 zero velocity
            twist = Twist()
            self.cmd_pub.publish(twist)
            self.get_logger().warn('No ArUco marker detected. Publishing zero velocity.')
            return

        for i, marker_id in enumerate(ids.flatten()):
            if marker_id == 5:
                rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
                    corners[i], self.marker_length, self.K, self.D)

                cv2.drawFrameAxes(frame, self.K, self.D, rvec, tvec, 0.1)

                if len(rvec) > 0 and len(tvec) > 0:
                    x, y, z = tvec[0][0]

                    # 取得 rotation vector 並轉換為角度
                    rx, ry, rz = rvec[0][0]
                    rz_deg = math.degrees(rz)
                    x_error = x + 0.03

                    # 控制誤差與指令
                    angular_z_error = abs(rz_deg) - 45
                    linear_x = self.linear_k * (z - self.target_distance)
                    linear_y = self.lateral_k * x_error
                    angular_z = -self.angular_k * angular_z_error


                    if abs(z - self.target_distance) < 0.02 and abs(x_error) < 0.02 and abs(angular_z_error) < 2:
                        self.cmd_pub.publish(Twist())
                        self.success_count += 1
                        self.get_logger().info('Arrived at target position.')
                        if self.success_count >= 20:
                            self.get_logger().info('Reached 20 successful arrivals. Shutting down node...')
                            rclpy.shutdown()

                        return
                    else:
                        self.success_count = 0
                    twist = Twist()
                    twist.linear.x = float(np.clip(linear_x, -0.2, 0.2))
                    twist.linear.y = float(np.clip(linear_y, -0.2, 0.2))
                    twist.angular.z = float(np.clip(angular_z, -0.5, 0.5))
                    self.cmd_pub.publish(twist)

                    self.get_logger().info(
                        f"Error x={x:.3f} m, z={z:.3f} m, angular_z={angular_z_error:.2f}°, "
                        f"Cmd x={linear_x:.2f}, y={linear_y:.2f}, w={angular_z:.2f}"
                    )
                    return


def main(args=None):
    rclpy.init(args=args)
    node = ArucoParkingNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
