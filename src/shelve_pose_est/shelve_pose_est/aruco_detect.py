import pyrealsense2 as rs
import numpy as np
import cv2
from cv2 import aruco
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
pipeline.start(config)

# Variables for FPS calculation
frame_count = 0
start_time = time.time()
fps = 0

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

def estimate_pose(frame, corners, ids, marker_size=0.05, intrinsics=None):
    """
    Estimate pose of ArUco markers
    
    Args:
        frame: Input camera frame
        corners: Detected marker corners from detectMarkers
        ids: Marker IDs from detectMarkers
        marker_size: Physical size of the marker in meters (default 5cm)
        
    Returns:
        Frame with pose visualization drawn on it
    """
    if ids is None or len(ids) == 0:
        return frame
    
    # Use RealSense intrinsics if provided, otherwise use defaults
    if intrinsics is not None:
        # Get camera matrix from RealSense intrinsics
        camera_matrix = np.array([
            [intrinsics.fx, 0, intrinsics.ppx],
            [0, intrinsics.fy, intrinsics.ppy],
            [0, 0, 1]
        ], dtype=np.float32)
        
        # Get distortion coefficients from RealSense
        # Order: [k1, k2, p1, p2, k3]
        dist_coeffs = np.array([
            intrinsics.coeffs[0],  # k1
            intrinsics.coeffs[1],  # k2
            intrinsics.coeffs[2],  # p1
            intrinsics.coeffs[3],  # p2
            intrinsics.coeffs[4]   # k3
        ], dtype=np.float32).reshape((5, 1))
    else:
        # Fallback to placeholder values
        fx, fy = frame.shape[1]/2, frame.shape[1]/2
        cx, cy = frame.shape[1]/2, frame.shape[0]/2
        camera_matrix = np.array([
            [fx, 0, cx],
            [0, fy, cy],
            [0, 0, 1]
        ], dtype=np.float32)
        dist_coeffs = np.zeros((5, 1), dtype=np.float32)
    
    # For each detected marker
    for i in range(len(ids)):
        # Estimate pose for current marker
        rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(
            corners[i], marker_size, camera_matrix, dist_coeffs
        )
        
        # Draw axis for the ArUco marker
        cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvec, tvec, marker_size/2)
        
        # Display marker position and orientation information
        marker_id = ids[i][0]
        position = tvec[0][0]
        position_text = f"ID:{marker_id} x:{position[0]:.4f} y:{position[1]:.4f} z:{position[2]:.4f}m"
        cv2.putText(frame, position_text, 
                    (int(corners[i][0][0][0]), int(corners[i][0][0][1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        '''Show marker position and rotation'''
        # If marker ID is 0, print its position and rotation to console
        if marker_id == 0:
            # Position is already in tvec
            position = tvec[0][0]
            
            # Convert rotation vector to rotation matrix and then to Euler angles
            rotation_matrix, _ = cv2.Rodrigues(rvec[0][0])
            euler_angles = cv2.decomposeProjectionMatrix(np.hstack((rotation_matrix, np.zeros((3,1)))))[6]
            
            # Print position (x,y,z) and rotation (rx,ry,rz) in degrees
            print(f"Marker 0 Position: x={position[0]:.5f}m, y={position[1]:.5f}m, z={position[2]:.5f}m")
            print(f"Marker 0 Rotation: rx={euler_angles[0][0]:.2f}°, ry={euler_angles[1][0]:.2f}°, rz={euler_angles[2][0]:.2f}°")
    
    return frame

try:
    # Get the intrinsics after starting the pipeline
    profile = pipeline.get_active_profile()
    color_profile = rs.video_stream_profile(profile.get_stream(rs.stream.color))
    color_intrinsics = color_profile.get_intrinsics()

    while True:
        # Wait for frames
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()
          
        # Convert images to numpy array
        color_image = np.asanyarray(color_frame.get_data())
        
        # Calculate FPS
        frame_count += 1
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # Update FPS counter every second
        if elapsed_time > 0.1:
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()

        # aruco detection
        detected_image, corners, ids = detect_aruco_marker(color_image)
        
        # Estimate ArUco pose
        pose_images = estimate_pose(color_image, corners , ids, intrinsics=color_intrinsics)
        
        # Display FPS on the image
        fps_text = f"FPS: {fps:.1f}"
        cv2.putText(color_image, fps_text, (color_image.shape[1] - 150, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Resize to 50% of original size
        scale_percent = 50
        width = int(color_image.shape[1] * scale_percent / 100)
        height = int(color_image.shape[0] * scale_percent / 100)
        resized_image = cv2.resize(color_image, (width, height))

        # Display the image
        cv2.imshow('RealSense', resized_image)
        
        # Exit if ESC pressed
        if cv2.waitKey(1) == 27:
            break
finally:
    pipeline.stop()

