import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose, PoseArray
from interface.srv import Maincontroller
from cv_bridge import CvBridge
import os
import configparser

import numpy as np
from scipy.spatial.transform import Rotation as R
import cv2
from cv2 import aruco
import time

# Define the offset for marker ID 0 (in meters)
MARKER_0_OFFSET = {
    'x': 0.1,  # 10cm offset in x direction
    'y': 0.1,  # no offset in y direction
    'z': 0.0,  # 20cm offset in z direction
}

# Add function to read calibration
def read_camera_config(filepath):
    """Read camera intrinsics and distortion from an ini file."""
    parser = configparser.ConfigParser()
    parser.read(filepath)
    cm = parser['Intrinsic']
    camera_matrix = np.array([
        [float(cm['0_0']), float(cm['0_1']), float(cm['0_2'])],
        [float(cm['1_0']), float(cm['1_1']), float(cm['1_2'])],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)
    dc = parser['Distortion']
    dist_coeffs = np.array([
        float(dc['k1']), float(dc['k2']), float(dc['t1']),
        float(dc['t2']), float(dc['k3'])
    ], dtype=np.float32)
    return camera_matrix, dist_coeffs

# Load calibration from ini next to this script
calib_file = os.path.join('src/shelf_pose_est/shelf_pose_est/azure_camera_calibration.ini')
cam_mtx, dist = read_camera_config(calib_file)

# Precompute OpenCV camera matrix and distortion coefficients once
CAMERA_MATRIX = cam_mtx.astype(np.float32)
DIST_COEFFS = dist.astype(np.float32).reshape((5, 1))

class ArucoDetect(Node):
    def __init__(self):
        super().__init__('aruco_detect_publisher')
        # self.publisher_ = self.create_publisher(PoseArray, 'aruco_detect', 10)
        # self.subscription = self.create_subscription(Image, '/camera/camera/color/image_raw', self.detect_aruco_callback, 10)
        self.publisher_ = None
        self.subscription = None
        self.srv = self.create_service(Maincontroller, '/toggle_aruco_detection', self.toggle_aruco_callback)

        self.bridge = CvBridge()

        # Variables for FPS calculation
        self.frame_count = 0
        self.start_time = time.time()
        self.fps = 0

        # Variables to track camera topic activity
        self.last_msg_time = None
        self.camera_check_timer = self.create_timer(3.0, self.check_camera_topic)

        # State of the Node
        self.active = False

    # response.done = 0
    def toggle_aruco_callback(self, request, response):
        # Activate publisher and subsciber
        if request.enable and not self.active:
            self.publisher_ = self.create_publisher(PoseArray, 'aruco_detect', 10)
            self.subscription = self.create_subscription(Image, '/camera/color/azure_image', self.detect_aruco_callback, 10)
            response.done = 0
            self.get_logger().info("ArUco detection activated")
            self.active = True
        # Deactivate publisher and subsciber
        elif not request.enable and self.active:
            self.destroy_publisher(self.publisher_)
            self.destroy_subscription(self.subscription)
            cv2.destroyAllWindows()
            response.done = True
            self.get_logger().info("ArUco detection deactivated")
            self.active = False
        # Same state as requested
        else:
            if self.active:
                state_str = "active"
            else:
                state_str = "inactive"
            response.done = 2
            self.get_logger().info(f"ArUco detection already {state_str}")
        return response

    def check_camera_topic(self):
        """Check if we've received camera messages recently"""
        if self.last_msg_time is None:
            self.get_logger().warn("\n" + "="*50 +
                                  "\nNo images received yet on /camera/camera/color/image_raw" +
                                  "\nPlease ensure camera is running" +
                                  "\nOr this node is not yet activated" +
                                  "\n" + "="*50)

    def detect_aruco_callback(self, msg):
        # Update the timestamp of the last received message
        self.last_msg_time = self.get_clock().now()

        color_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        max_marker_id = 8

        # Calculate FPS
        self.frame_count += 1
        end_time = time.time()
        elapsed_time = end_time - self.start_time

        # Update FPS counter every second
        if elapsed_time > 0.1:
            self.fps = self.frame_count / elapsed_time
            self.frame_count = 0
            self.start_time = time.time()

        # aruco detection
        detected_image, corners, ids = detect_aruco_marker(color_image)

        # Estimate ArUco pose
        pose_images, marker_poses = estimate_pose_and_get_data(color_image, corners, ids)

        # Initialize pose array with zeros
        self.pose_array = PoseArray()
        self.pose_array.header.stamp = self.get_clock().now().to_msg()
        self.pose_array.header.frame_id = "camera_color_optical_frame"

        # Create empty poses for each possible marker ID
        for i in range(max_marker_id):
            empty_pose = Pose()
            self.pose_array.poses.append(empty_pose)

        # Fill in the pose array with detected marker poses
        for i in range(len(marker_poses)):
            marker_data = marker_poses[i]
            marker_id = marker_data['id']

            # Skip if marker ID is outside our range
            if marker_id >= max_marker_id:
                self.get_logger().warn(f"Marker ID {marker_id} is out of range (max: {max_marker_id-1}). Skipping.")
                continue

            # Create Pose for this marker
            pose = Pose()

            # Set position
            position = marker_data['position']
            pose.position.x = position[0]
            pose.position.y = position[1]
            pose.position.z = position[2]

            # Set orientation (quaternion)
            r = R.from_matrix(marker_data['rotation_matrix'])
            quat = r.as_quat()  # [x, y, z, w] format
            pose.orientation.x = quat[0]
            pose.orientation.y = quat[1]
            pose.orientation.z = quat[2]
            pose.orientation.w = quat[3]

            self.pose_array.poses[marker_id] = pose

        # Publish the pose array
        self.publisher_.publish(self.pose_array)
        # self.get_logger().info(f"Pose array[0]: {self.pose_array.poses[0]}")
        # self.get_logger().info(f"Pose array[1]: {self.pose_array.poses[1]}")
        # self.get_logger().info(f"Pose array[2]: {self.pose_array.poses[2]}")
        # self.get_logger().info(f"Pose array[3]: {self.pose_array.poses[3]}")
        # self.get_logger().info(f"Pose array[4]: {self.pose_array.poses[4]}")
        # self.get_logger().info(f"Pose array[5]: {self.pose_array.poses[5]}")
        # self.get_logger().info(f"Pose array[6]: {self.pose_array.poses[6]}")
        # self.get_logger().info(f"Pose array[7]: {self.pose_array.poses[7]}")

        # Display FPS on the image
        fps_text = f"FPS: {self.fps:.1f}"
        cv2.putText(color_image, fps_text, (color_image.shape[1] - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Resize to 50% of original size
        # scale_percent = 50
        # width = int(color_image.shape[1] * scale_percent / 100)
        # height = int(color_image.shape[0] * scale_percent / 100)
        # resized_image = cv2.resize(color_image, (width, height))

        # Display the image
        cv2.namedWindow('ArUco detector', cv2.WINDOW_NORMAL)
        cv2.imshow('ArUco detector', color_image)

        # Exit if ESC pressed
        if cv2.waitKey(1) == 27:
            self.destroy_publisher(self.publisher_)
            self.destroy_subscription(self.subscription)
            cv2.destroyAllWindows()
            # self.destroy_node()
            # rclpy.shutdown()


# Get the intrinsics after starting the pipeline
def detect_aruco_marker(frame, dictionary_type = aruco.DICT_6X6_50):
    """
    Detect ArUco markers in camera frames

    Args:
        frame: camera frame, numpy array
        dictionary_type: ArUco dictionary type to use for detection
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.getPredefinedDictionary(dictionary_type)
    corners, ids, rejected = aruco.detectMarkers(gray, arucoDict)
    aruco.drawDetectedMarkers(frame, corners, ids)

    return frame, corners, ids

def estimate_pose_and_get_data(frame, corners, ids, marker_size=0.10):
    """
    Estimate pose of ArUco markers

    Args:
        frame: Input camera frame
        corners: Detected marker corners from detectMarkers
        ids: Marker IDs from detectMarkers
        marker_size: Physical size of the marker in meters (default 5cm)

    Returns:
        Frame with pose visualization drawn on it and list of marker poses
    """
    marker_poses = []
    if ids is None or len(ids) == 0:
        return frame, marker_poses

    # Use precomputed RealSense intrinsics
    camera_matrix = CAMERA_MATRIX
    dist_coeffs = DIST_COEFFS

    # For each detected marker
    for i, id in enumerate(ids):
        # Estimate pose for current marker
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners[i], marker_size, camera_matrix, dist_coeffs
        )

        # Get marker ID and position
        marker_id = ids[i][0]
        position = tvec[0][0]

        # Convert rotation vector to rotation matrix
        rotation_matrix, _ = cv2.Rodrigues(rvec[0][0])

        # Store pose data for this marker
        marker_poses.append({
            'id': marker_id,
            'position': position,
            'rotation_matrix': rotation_matrix
        })

        # Draw axis for each ArUco marker
        cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_size/2)

        # If marker ID is 0, print its position and rotation to console
        # and draw the offset axis
        if marker_id == 0:
            # Position is already in tvec
            position = tvec[0][0]

            # Display marker position and orientation information
            position_text = f"ID:{marker_id} x:{position[0]:.4f} y:{position[1]:.4f} z:{position[2]:.4f}m"
            cv2.putText(frame, position_text,
                        (int(corners[i][0][0][0]), int(corners[i][0][0][1]) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Convert rotation vector to rotation matrix
            rotation_matrix, _ = cv2.Rodrigues(rvec[0][0])

            # Convert rotation matrix to Euler angles
            euler_angles = cv2.decomposeProjectionMatrix(np.hstack((rotation_matrix, np.zeros((3,1)))))[6]

            # Print position (x,y,z) and rotation (rx,ry,rz) in degrees
            print(f"Marker 0 Position: x={position[0]:.5f}m, y={position[1]:.5f}m, z={position[2]:.5f}m")
            print(f"Marker 0 Rotation: rx={euler_angles[0][0]:.2f}°, ry={euler_angles[1][0]:.2f}°, rz={euler_angles[2][0]:.2f}°")

            # Calculate the offset position relative to marker 0
            # Apply the rotation matrix to the offset vector
            offset_vector = np.array([
                [MARKER_0_OFFSET['x']],
                [MARKER_0_OFFSET['y']],
                [MARKER_0_OFFSET['z']]
            ])

            # Apply the rotation matrix to transform the offset to the marker's coordinate system
            rotated_offset = np.dot(rotation_matrix, offset_vector)

            # Add the rotated offset to the marker's position
            offset_position = position + rotated_offset.flatten()

            # Create a new translation vector for the offset axis
            offset_tvec = np.array([[offset_position]], dtype=np.float32)

            # Draw the offset axis (using a larger axis size for visibility)
            cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, offset_tvec, marker_size/2)

            # Display offset position information
            offset_text = f"Offset: x:{offset_position[0]:.4f} y:{offset_position[1]:.4f} z:{offset_position[2]:.4f}m"
            cv2.putText(frame, offset_text,
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    return frame, marker_poses

def main():
    rclpy.init()
    aruco_detect = ArucoDetect()
    rclpy.spin(aruco_detect)
    aruco_detect.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
