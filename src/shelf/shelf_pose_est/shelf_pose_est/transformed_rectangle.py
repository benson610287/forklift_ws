import cv2
import numpy as np
import math

# Your camera intrinsics
CAMERA_MATRIX = np.array([
    [913.201294, 0.000000, 961.154724],
    [0.000000, 912.630859, 552.623535],
    [0.000000, 0.000000, 1.000000]
])

# Extract intrinsic parameters
FX = CAMERA_MATRIX[0, 0]  # 913.201294
FY = CAMERA_MATRIX[1, 1]  # 912.630859
CX = CAMERA_MATRIX[0, 2]  # 961.154724
CY = CAMERA_MATRIX[1, 2]  # 552.623535

def create_3d_rotation_matrix(rx, ry, rz):
    """
    Create a 3D rotation matrix for rotations around x, y, and z axes
    rx, ry, rz: rotation angles in degrees
    """
    # Convert degrees to radians
    rx_rad = math.radians(rx)
    ry_rad = math.radians(ry)
    rz_rad = math.radians(rz)

    # Rotation matrix around X-axis
    Rx = np.array([
        [1, 0, 0],
        [0, math.cos(rx_rad), -math.sin(rx_rad)],
        [0, math.sin(rx_rad), math.cos(rx_rad)]
    ])

    # Rotation matrix around Y-axis
    Ry = np.array([
        [math.cos(ry_rad), 0, math.sin(ry_rad)],
        [0, 1, 0],
        [-math.sin(ry_rad), 0, math.cos(ry_rad)]
    ])

    # Rotation matrix around Z-axis
    Rz = np.array([
        [math.cos(rz_rad), -math.sin(rz_rad), 0],
        [math.sin(rz_rad), math.cos(rz_rad), 0],
        [0, 0, 1]
    ])

    # Combined rotation matrix (order: Rz * Ry * Rx)
    R = np.dot(Rz, np.dot(Ry, Rx))
    return R

def project_3d_to_2d(points_3d, fx=FX, fy=FY, center_x=CX, center_y=CY):
    """
    Project 3D points to 2D using perspective projection with camera intrinsics
    """
    points_2d = []
    for point in points_3d:
        x, y, z = point
        # Standard perspective projection
        if z != 0:  # Avoid division by zero
            x_proj = int(fx * x / z + center_x)
            y_proj = int(fy * y / z + center_y)
        else:
            x_proj = int(x + center_x)
            y_proj = int(y + center_y)
        points_2d.append([x_proj, y_proj])
    return np.array(points_2d, dtype=np.int32)

def rotate_rectangle_3d(rx, ry, rz, rect_size=100, center_3d=(0, 0, 500)):
    """
    Create and rotate a 3D rectangle
    rx, ry, rz: rotation angles in degrees
    rect_size: size of the rectangle
    center_3d: center point in 3D space (moved further from camera)
    """
    # Create a black image with size matching your camera resolution
    image = np.zeros((1080, 1920, 3), dtype=np.uint8)

    # Define the rectangle's corners in 3D space (centered at origin)
    half_size = rect_size // 2
    rect_3d = np.array([
        [-half_size, -half_size, 0],  # Bottom-left
        [half_size, -half_size, 0],   # Bottom-right
        [half_size, half_size, 0],    # Top-right
        [-half_size, half_size, 0]    # Top-left
    ], dtype=np.float32)

    # Get the 3D rotation matrix
    R = create_3d_rotation_matrix(rx, ry, rz)

    # Apply rotation to each point
    rotated_points_3d = []
    for point in rect_3d:
        rotated_point = np.dot(R, point)
        # Translate to the desired center
        rotated_point += center_3d
        rotated_points_3d.append(rotated_point)

    # Project 3D points to 2D using camera intrinsics
    points_2d = project_3d_to_2d(rotated_points_3d)

    # Draw the transformed rectangle
    cv2.polylines(image, [points_2d], True, (0, 255, 0), 2)  # Green outline

    # Add coordinate axes for reference
    draw_axes(image, center_3d, R)

    # Add text showing rotation values and camera info
    cv2.putText(image, f"rx: {rx}°, ry: {ry}°, rz: {rz}°",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, f"fx: {FX:.1f}, fy: {FY:.1f}",
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(image, f"cx: {CX:.1f}, cy: {CY:.1f}",
                (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    return image

def draw_axes(image, center_3d, rotation_matrix, length=200):
    """
    Draw coordinate axes to show orientation
    """
    # Define axis vectors
    axes_3d = np.array([
        [length, 0, 0],  # X-axis (red)
        [0, length, 0],  # Y-axis (green)
        [0, 0, length]   # Z-axis (blue)
    ])

    # Apply rotation to axes
    rotated_axes = []
    for axis in axes_3d:
        rotated_axis = np.dot(rotation_matrix, axis)
        rotated_axes.append(rotated_axis + center_3d)

    # Project to 2D using camera intrinsics
    origin_2d = project_3d_to_2d([center_3d])[0]
    axes_2d = project_3d_to_2d(rotated_axes)

    # Draw axes
    colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]  # Red, Green, Blue
    labels = ['X', 'Y', 'Z']

    for i, (axis_2d, color, label) in enumerate(zip(axes_2d, colors, labels)):
        cv2.line(image, tuple(origin_2d), tuple(axis_2d), color, 2)
        cv2.putText(image, label, tuple(axis_2d), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Example usage
if __name__ == "__main__":
    """
    # Test with different rotation values
    rx, ry, rz = 30, 45, 60  # Rotation angles in degrees

    # Create and display the rotated rectangle
    image = rotate_rectangle_3d(rx, ry, rz)

    cv2.imshow("3D Rotated Rectangle", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """

    # Interactive rotation with trackbars
    cv2.namedWindow("3D Rotated Rectangle")
    cv2.createTrackbar("RX", "3D Rotated Rectangle", 0, 360, lambda x: None)
    cv2.createTrackbar("RY", "3D Rotated Rectangle", 0, 360, lambda x: None)
    cv2.createTrackbar("RZ", "3D Rotated Rectangle", 0, 360, lambda x: None)
    cv2.createTrackbar("Distance", "3D Rotated Rectangle", 500, 1000, lambda x: None)

    while True:
        rx = cv2.getTrackbarPos("RX", "3D Rotated Rectangle")
        ry = cv2.getTrackbarPos("RY", "3D Rotated Rectangle")
        rz = cv2.getTrackbarPos("RZ", "3D Rotated Rectangle")
        distance = cv2.getTrackbarPos("Distance", "3D Rotated Rectangle")

        # Use distance for z-coordinate
        center_3d = (0, 0, distance)

        image = rotate_rectangle_3d(rx, ry, rz, center_3d=center_3d)
        h, w = image.shape[:2]
        resized = cv2.resize(image, (int(w/2), int(h/2)))
        cv2.imshow('3D Rotated Rectangle', resized)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
