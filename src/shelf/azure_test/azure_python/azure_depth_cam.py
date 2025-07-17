import cv2
import numpy as np
import pyk4a
from pyk4a import Config, PyK4A
from typing import Optional, Tuple
import time

max_depth_value = 6000

def on_max_depth_change(val):
    global max_depth_value
    max_depth_value = val
    cv2.setTrackbarPos('Max Depth', 'k4a depth viewer', max_depth_value)

def create_control_panel():
    global max_depth_value
    cv2.namedWindow('k4a depth viewer', cv2.WINDOW_NORMAL)
    cv2.createTrackbar('Max Depth', 'k4a depth viewer', max_depth_value, 6000, on_max_depth_change)

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

def main():
    global max_depth_value

    config = Config()
    config.color_resolution = pyk4a.ColorResolution.RES_1080P
    # config.color_resolution = pyk4a.ColorResolution.OFF
    config.depth_mode = pyk4a.DepthMode.NFOV_UNBINNED
    config.synchronized_images_only = True

    k4a = PyK4A(config)
    k4a.start()

    create_control_panel()

    frame_count = 0
    start_time = time.time()
    last_frame_time = None
    print("print 'q' to exit camera")
    while True:
        capture = k4a.get_capture()
        if capture.transformed_depth is not None:
            frame_count += 1
            current_time = time.time()
            #color image
            # color_image = capture.color[:, :, :3]
            # color_image = np.array(color_image, dtype=np.uint8)
            # depth image
            depth_image = colorize_depth(capture.transformed_depth)

            #combine depth, color then display
            # combine = np.hstack((color_image, depth_image))

            if last_frame_time is not None:
                fps = 1.0/(current_time - last_frame_time)
                cv2.putText(depth_image, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
            last_frame_time = current_time

            cv2.namedWindow('k4a depth viewer', cv2.WINDOW_NORMAL)
            cv2.imshow('k4a depth viewer', depth_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
    k4a.stop()
    print(capture.transformed_depth[1000, 700])
    height, width = capture.transformed_depth.shape
    print(height)
    print(width)

if __name__ == "__main__":
    main()
