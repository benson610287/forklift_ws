# from typing import AsyncGenerator
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
# from geometry_msgs.msg import Pose
from interface.msg import ShelfState
from interface.srv import Maincontroller
from cv_bridge import CvBridge

import numpy as np
import cv2
# import time
from ultralytics import YOLO
import os

max_depth_value = 6000

def on_max_depth_change(val):
    global max_depth_value
    max_depth_value = val
    cv2.setTrackbarPos('Max Depth', 'Depth Image', max_depth_value)

def create_control_panel():
    global max_depth_value
    cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Max Depth', 'Depth Image', max_depth_value, 6000, on_max_depth_change)

def colorize_depth(depth_image: np.ndarray,
    min_depth=0, max_depth=6000,
    colormap = cv2.COLORMAP_OCEAN) -> np.ndarray:
    """
    Colorize depth image using OpenCV colormaps

    Args:transformed_depth
        depth_image: Raw depth image (16-bit or float)
        min_depth: Minimum depth value for normalization
        max_depth: Maximum depth value for normalization
        colormap: OpenCV Colormaps
            # Popular colormaps for depth
            cv2.COLORMAP_JET        # Blue -> Green -> Yellow -> Red
            cv2.COLORMAP_HOT        # Black -> Red -> Yellow -> White
            cv2.COLORMAP_RAINBOW    # Purple -> Blue -> Green -> Yellow -> Red
            cv2.COLORMAP_VIRIDIS    # Purple -> Blue -> Green -> Yellow
            cv2.COLORMAP_PLASMA     # Purple -> Pink -> Yellow
            cv2.COLORMAP_INFERNO    # Black -> Purple -> Red -> Yellow
            cv2.COLORMAP_MAGMA      # Black -> Purple -> Pink -> White
            cv2.COLORMAP_OCEAN      # Black -> Blue -> Cyan -> Yellow
            cv2.COLORMAP_COOL       # Cyan -> Magenta
            cv2.COLORMAP_SPRING     # Magenta -> Yellow
            cv2.COLORMAP_SUMMER     # Green -> Yellow
            cv2.COLORMAP_AUTUMN     # Red -> Yellow
            cv2.COLORMAP_WINTER     # Blue -> Green
            cv2.COLORMAP_BONE       # Black -> White (bone-like)
            cv2.COLORMAP_PINK       # Black -> Pink -> White
            cv2.COLORMAP_HSV        # Red -> Yellow -> Green -> Cyan -> Blue -> Magenta
            cv2.COLORMAP_PARULA     # Blue -> Cyan -> Yellow -> Orange
            cv2.COLORMAP_TURBO      # Blue -> Cyan -> Green -> Yellow -> Red

    Returns:
        Colorized depth image (BGR format)
    """
    if depth_image is None:
        return None

    # Use track bar value
    global max_depth_value
    max_depth = max_depth_value

    # Remove invalid depth values (0 means no depth data)
    depth_clean = depth_image.copy()
    depth_clean[depth_clean == 0] = max_depth

    # Normalize depth to 0-255 range
    depth_normalized = np.clip((depth_clean - min_depth) / (max_depth - min_depth), 0, 1)
    depth_uint8 = (depth_normalized * 255).astype(np.uint8)

    # Apply colormap
    depth_colorized = cv2.applyColorMap(depth_uint8, colormap)

    return depth_colorized

class ShelfPointDetector(Node):
    def __init__(self):
        super().__init__('shelf_state_publisher')

        self.subscription = self.create_subscription(Image, '/camera/color/azure_image', self.shelf_point_detect_callback, 10)
        self.depth_subscription = self.create_subscription(Image, '/camera/depth/azure_depth', self.depth_frame_callback, 10)
        self.shelf_state_publisher = self.create_publisher(ShelfState, '/shelf/state', 10)
        self.shelf_depth_publisher = self.create_publisher(Image, '/camera/depth/state_image', 10)
        self.bridge = CvBridge()

        # Load YOLO model
        model_file = "./src/shelf/shelf_pose_est/shelf_yolo_weights/last-pose.engine"
        if os.path.exists(model_file):
            self.get_logger().info("Loading Model")
            self.tensorrt_model = YOLO(model_file)
        else:
            model = YOLO("./src/shelf/shelf_pose_est/shelf_yolo_weights/last-pose.pt")
            model.export(format="engine")
            self.tensorrt_model = YOLO(model_file)

        # depth detection config
        self.detect_depth = 4500

        create_control_panel()

    def shelf_point_detect_callback(self, color_msg):

        color_image = self.bridge.imgmsg_to_cv2(color_msg, 'bgr8')
        results = self.tensorrt_model(color_image)

        for result in results:
            self.xy = result.keypoints.xy

        annotated_frame = results[0].plot()
        cv2.namedWindow('YOLO Shelf Keypoint', cv2.WINDOW_NORMAL)
        cv2.imshow('YOLO Shelf Keypoint', annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.destroy_subscription(self.subscription)
            self.destroy_subscription(self.depth_subscription)
            cv2.destroyAllWindows()

    def depth_frame_callback(self, depth_msg):
        msg = ShelfState()
        self.depth = self.bridge.imgmsg_to_cv2(depth_msg, 'passthrough')
        depth_image = colorize_depth(self.depth)
        # make sure self.xy and not empty
        if hasattr(self, 'xy') and self.xy is not None and len(self.xy) > 0:
            shelf_state = self.draw_shelf_polylines(depth_image, self.xy)
            # print("SHELF STATE: ",shelf_state)
            msg.shelf_state = shelf_state.astype(bool).tolist()
            self.shelf_state_publisher.publish(msg)
            depth_state_msg = self.bridge.cv2_to_imgmsg(depth_image, 'passthrough')
            self.shelf_depth_publisher.publish(depth_state_msg)
        cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)
        cv2.imshow('Depth Image', depth_image)


    def count_pixels_in_polygon(self, image, polygon_points, min_valid_depth=100, max_valid_depth=6000, detect_depth=5500):
        # Create mask
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [polygon_points], 255)

        roi_pixels = image[mask>0]
        invalid_pixels = image[mask==0]
        # Count valid pixels within the polygon
        valid_pixels = roi_pixels[(roi_pixels >= min_valid_depth) & (roi_pixels <= max_valid_depth)]
        # Count pixels that are within the detection depth range
        detect_pixels = roi_pixels[(roi_pixels >= min_valid_depth) & (roi_pixels <= detect_depth)]

        valid_pixels_count = len(valid_pixels)
        detect_pixels_count = len(detect_pixels)
        invalid_pixels_count = len(invalid_pixels)
        if valid_pixels_count == 0:
            return 0.0, 0.0, 0.0
        detect_ratio = detect_pixels_count/valid_pixels_count
        invalid_ratio = invalid_pixels_count/valid_pixels_count

        return detect_ratio, invalid_ratio, detect_pixels_count

    def draw_shelf_polylines(self, image, xy_tensor):

        """Draw polylines from YOLO keypoint tensor"""
        # Convert tensor to numpy and move to CPU
        all_shelfs_keypoints = xy_tensor.cpu().numpy()

        # rearange xy_numpy
        first_x_values = all_shelfs_keypoints[:, 0, 0] # Shape: (4,) - first x-coord of each object
        sort_indices = np.argsort(first_x_values)
        temp_shelfs = all_shelfs_keypoints[sort_indices]

        mid_point = all_shelfs_keypoints.shape[0]//2
        first_half = temp_shelfs[ :mid_point]
        second_half = temp_shelfs[mid_point: ]
        # Sort by first point's y-coordinate of each object
        first_y_values = first_half[: ,0, 1]
        sort_indices = np.argsort(first_y_values)
        sorted_first_half = first_half[sort_indices]

        first_y_values = second_half[: ,0, 1]
        sort_indices = np.argsort(first_y_values)
        sorted_second_half = second_half[sort_indices]

        sorted_shelfs_keypoints = np.concatenate([sorted_first_half, sorted_second_half], axis=0)
        # Draw each shelf section
        sorted_polygon_points = []
        shelf_state = np.zeros(8)
        state_index = 0
        for i, each_shelf_points in enumerate(sorted_shelfs_keypoints):
            if i == 1 or i == 3:
                each_shelf_points[1][1]-=10
                each_shelf_points[2][1]-=10

            each_shelf_points[0][1]+=10
            each_shelf_points[3][1]+=10
            top_mid_point = (each_shelf_points[0]+each_shelf_points[3])/2
            bottom_mid_point = (each_shelf_points[1]+each_shelf_points[2])/2
            left_shelf = np.array([each_shelf_points[0], each_shelf_points[1], bottom_mid_point, top_mid_point])
            right_shelf = np.array([top_mid_point, bottom_mid_point, each_shelf_points[2], each_shelf_points[3]])
            each_shelf = np.array([left_shelf, right_shelf])



            for j, sub_shelf in enumerate(each_shelf):
                # Convert to integer coordinates
                points = sub_shelf.astype(int)
                # Convert to proper format for cv2.polylines
                polygon_points = points.reshape((-1, 1, 2))
                # Draw polygon outline
                detected_ratio, invalid_ratio, detected_pixels_count = self.count_pixels_in_polygon(self.depth, polygon_points, detect_depth=self.detect_depth)
                print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                print(f"detected ratio {state_index}: ",detected_ratio)
                print(f"invalid ratio {state_index}: ",invalid_ratio)
                print(f"detected pixels {state_index}: ",detected_pixels_count)
                if state_index < 8:
                    # the blow magic ratio number is tested with specific angle
                    if detected_ratio >= 0.06 or detected_pixels_count >= 600:
                        # red: have stuff on shelf
                        cv2.polylines(image, [polygon_points], True, (0, 0, 255), 3)
                        shelf_state[state_index] = False
                    else:
                        # green: no stuff on shelf
                        cv2.polylines(image, [polygon_points], True, (0, 255, 0), 3)
                        shelf_state[state_index] = True

                        sorted_polygon_points.append(polygon_points)
                    state_index += 1
                else:
                    break

                # Add shelf label
                label_x, label_y = points[0][0], points[0][1] - 10
                cv2.putText(image, f'Shelf {i+1}-{j+1}', (label_x, label_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

                # for adjusting parameters
                label_x, label_y = points[0][0]+10, points[0][1] - 20
                cv2.putText(image, f"{detected_pixels_count}", (label_x, label_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

        return shelf_state


def main():
    rclpy.init()
    shelf_keypoint_detect = ShelfPointDetector()
    rclpy.spin(shelf_keypoint_detect)
    shelf_keypoint_detect.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
