import cv2
import pyk4a
import time
from pyk4a import Config, PyK4A, ColorControlCommand, ColorControlMode
import numpy as np

def digital_zoom(image, zoom_factor, center=None):
    """Apply digital zoom to an image"""
    height, width = image.shape[:2]

    if center is None:
        center = (width // 2, height // 2)

    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)

    left = max(0, center[0] - new_width // 2)
    top = max(0, center[1] - new_height // 2)
    right = min(width, left + new_width)
    bottom = min(height, top + new_height)

    cropped = image[top:bottom, left:right]
    zoomed = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_CUBIC)

    return zoomed

def set_focus_manual(device, focus_value):
    """Set manual focus using pyk4a API"""
    try:
        device._set_color_control(ColorControlCommand.FOCUS, focus_value, ColorControlMode.MANUAL)
        print(f"Focus set to MANUAL: {focus_value}")
        return True
    except Exception as e:
        print(f"Failed to set manual focus: {e}")
        return False

def set_focus_auto(device):
    """Set auto focus using pyk4a API"""
    try:
        device._set_color_control(ColorControlCommand.FOCUS, 0, ColorControlMode.AUTO)
        print("Focus set to AUTO")
        return True
    except Exception as e:
        print(f"Failed to set auto focus: {e}")
        return False

def get_focus_info(device):
    """Get current focus settings"""
    try:
        value, mode = device._get_color_control(ColorControlCommand.FOCUS)
        mode_str = "AUTO" if mode == ColorControlMode.AUTO else "MANUAL"
        return value, mode_str
    except Exception as e:
        print(f"Failed to get focus info: {e}")
        return None, None

def get_focus_capabilities(device):
    """Get focus control capabilities"""
    try:
        caps = device._get_color_control_capabilities(ColorControlCommand.FOCUS)
        return caps
    except Exception as e:
        print(f"Failed to get focus capabilities: {e}")
        return None

def main():
    """Main function with pyk4a focus control"""

    # Check device availability
    device_count = pyk4a.connected_device_count()
    if device_count == 0:
        print("No Azure Kinect devices found!")
        return

    print(f"Found {device_count} Azure Kinect device(s)")

    # Configure device
    config = Config()
    config.color_resolution = pyk4a.ColorResolution.RES_1080P
    config.depth_mode = pyk4a.DepthMode.NFOV_UNBINNED
    config.camera_fps = pyk4a.FPS.FPS_30
    config.synchronized_images_only = False

    # Initialize device
    k4a = PyK4A(config)
    k4a.start()

    print("\nAzure Kinect DK - pyk4a with Focus Control")
    print("=" * 50)
    print("Controls:")
    print("  'q' - Quit")
    print("  'a' - Auto focus")
    print("  'f' - Manual focus (far)")
    print("  'n' - Manual focus (near)")
    print("  '+' - Increase focus")
    print("  '-' - Decrease focus")
    print("  'r' - Reset focus to default")
    print("  'i' - Show focus info")
    print("  'c' - Show focus capabilities")
    print("  'z' - Zoom in")
    print("  'x' - Zoom out")
    print("  '1-5' - Set zoom levels")
    print("  'SPACE' - Screenshot")
    print("=" * 50)

    # Initialize settings
    zoom_factor = 1.0
    zoom_step = 0.2
    max_zoom = 5.0
    min_zoom = 0.5
    current_focus = 500  # Default focus value
    focus_step = 50
    screenshot_count = 0

    # Get focus capabilities
    focus_caps = get_focus_capabilities(k4a)
    if focus_caps:
        print(f"Focus capabilities: {focus_caps}")
        min_focus = focus_caps.get('min_value', 0)
        max_focus = focus_caps.get('max_value', 1000)
        default_focus = focus_caps.get('default_value', 500)
        current_focus = default_focus
    else:
        min_focus, max_focus = 0, 1000

    # Set initial focus
    set_focus_manual(k4a, current_focus)

    frame_count = 0
    start_time = time.time()
    last_frame_time = None

    try:
        while True:
            capture = k4a.get_capture()

            if capture.color is not None:
                frame_count += 1
                current_time = time.time()

                # Get the color image
                color_image = capture.color[:, :, :3]
                color_image = np.array(color_image, dtype=np.uint8)

                # Apply digital zoom
                display_image = color_image.copy()
                if zoom_factor != 1.0:
                    height, width = display_image.shape[:2]
                    zoom_center = (width // 2, height // 2)
                    display_image = digital_zoom(display_image, zoom_factor, zoom_center)

                # Calculate and display FPS
                if last_frame_time is not None:
                    frame_fps = 1.0 / (current_time - last_frame_time)
                    cv2.putText(display_image, f"FPS: {frame_fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

                # Display current settings
                cv2.putText(display_image, f"Zoom: {zoom_factor:.1f}x", (10, 70),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 255), 2)

                # Get and display current focus
                focus_value, focus_mode = get_focus_info(k4a)
                if focus_value is not None:
                    cv2.putText(display_image, f"Focus: {focus_value} ({focus_mode})", (10, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
                else:
                    cv2.putText(display_image, f"Focus: {current_focus} (MANUAL)", (10, 110),
                               cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

                last_frame_time = current_time

                # Display image
                cv2.namedWindow('Azure Kinect - Focus & Zoom Control', cv2.WINDOW_NORMAL)
                cv2.imshow('Azure Kinect - Focus & Zoom Control', display_image)

                # Handle key presses
                key = cv2.waitKey(1) & 0xFF

                if key == ord('q'):
                    break
                elif key == ord('a'):
                    # Auto focus
                    if set_focus_auto(k4a):
                        current_focus = -1  # Indicate auto mode
                elif key == ord('f'):
                    # Manual focus - far
                    current_focus = max_focus
                    set_focus_manual(k4a, current_focus)
                elif key == ord('n'):
                    # Manual focus - near
                    current_focus = min_focus
                    set_focus_manual(k4a, current_focus)
                elif key == ord('+') or key == ord('='):
                    # Increase focus
                    if current_focus != -1:  # Not in auto mode
                        current_focus = min(max_focus, current_focus + focus_step)
                        set_focus_manual(k4a, current_focus)
                elif key == ord('-'):
                    # Decrease focus
                    if current_focus != -1:  # Not in auto mode
                        current_focus = max(min_focus, current_focus - focus_step)
                        set_focus_manual(k4a, current_focus)
                elif key == ord('r'):
                    # Reset focus to default
                    current_focus = focus_caps.get('default_value', 500) if focus_caps else 500
                    set_focus_manual(k4a, current_focus)
                elif key == ord('i'):
                    # Show focus info
                    focus_value, focus_mode = get_focus_info(k4a)
                    if focus_value is not None:
                        print(f"Current focus: {focus_value} (Mode: {focus_mode})")
                    else:
                        print("Unable to get focus information")
                elif key == ord('c'):
                    # Show focus capabilities
                    if focus_caps:
                        print("Focus capabilities:")
                        for key_name, value in focus_caps.items():
                            print(f"  {key_name}: {value}")
                    else:
                        print("Focus capabilities not available")
                elif key == ord('z'):
                    # Zoom in
                    zoom_factor = min(max_zoom, zoom_factor + zoom_step)
                    print(f"Zoom: {zoom_factor:.1f}x")
                elif key == ord('x'):
                    # Zoom out
                    zoom_factor = max(min_zoom, zoom_factor - zoom_step)
                    print(f"Zoom: {zoom_factor:.1f}x")
                elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                    # Set specific zoom levels
                    zoom_factor = float(chr(key))
                    print(f"Zoom: {zoom_factor:.1f}x")
                elif key == ord(' '):  # Spacebar
                    # Take screenshot
                    screenshot_count += 1
                    filename = f"kinect_focus_zoom_{screenshot_count:03d}.jpg"
                    cv2.imwrite(filename, display_image)
                    print(f"Screenshot saved: {filename}")

    except KeyboardInterrupt:
        print("\nInterrupted by user")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Final statistics
        total_time = time.time() - start_time
        if frame_count > 0:
            final_fps = frame_count / total_time
            print(f"\nFinal Statistics:")
            print(f"  Frames captured: {frame_count}")
            print(f"  Total time: {total_time:.2f} seconds")
            print(f"  Average FPS: {final_fps:.2f}")
            if screenshot_count > 0:
                print(f"  Screenshots taken: {screenshot_count}")

        # Cleanup
        cv2.destroyAllWindows()
        k4a.stop()
        print("Camera stopped successfully")

if __name__ == "__main__":
    main()
