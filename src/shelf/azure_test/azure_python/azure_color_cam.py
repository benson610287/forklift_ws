import cv2
import pyk4a
import time
from pyk4a import Config, PyK4A
import numpy as np

def set_focus_mode(k4a_device, focus_value=None):
    """
    Set focus mode for Azure Kinect
    focus_value: None for auto focus, or integer value for manual focus (typically 0-1000)
    """
    try:
        if focus_value is None:
            # Set to auto focus
            k4a_device.set_color_control(pyk4a.ColorControlCommand.AUTO_EXPOSURE_PRIORITY,
                                       pyk4a.ColorControlMode.AUTO)
            print("Focus set to AUTO mode")
        else:
            # Set to manual focus with specified value
            k4a_device.set_color_control(pyk4a.ColorControlCommand.FOCUS,
                                       pyk4a.ColorControlMode.MANUAL,
                                       focus_value)
            print(f"Focus set to MANUAL mode with value: {focus_value}")
    except Exception as e:
        print(f"Error setting focus: {e}")

def get_current_focus(k4a_device):
    """Get current focus settings"""
    try:
        focus_info = k4a_device.get_color_control(pyk4a.ColorControlCommand.FOCUS)
        return focus_info
    except Exception as e:
        print(f"Error getting focus info: {e}")
        return None

def main():
    """Main function with focus control"""
    config = Config()
    config.color_resolution = pyk4a.ColorResolution.RES_1080P
    config.camera_fps = pyk4a.FPS.FPS_30
    config.synchronized_images_only = False

    k4a = PyK4A(config)
    k4a.start()

    print("Azure Kinect DK Camera with Focus Control")
    print("Controls:")
    print("  'q' - Quit")
    print("  'a' - Auto focus")
    print("  'f' - Manual focus (far)")
    print("  'n' - Manual focus (near)")
    print("  '+' - Increase focus")
    print("  '-' - Decrease focus")
    print("  'r' - Reset to default focus")
    print("  'i' - Show current focus info")

    # Initialize focus settings
    current_focus = 500  # Default manual focus value (adjust as needed)
    focus_step = 50      # Step size for focus adjustment

    # Set initial focus mode (you can change this)
    set_focus_mode(k4a, current_focus)  # Start with manual focus
    # set_focus_mode(k4a, None)  # Uncomment for auto focus

    frame_count = 0
    start_time = time.time()
    last_frame_time = None

    while True:
        capture = k4a.get_capture()

        if capture.color is not None:
            frame_count += 1
            current_time = time.time()

            # Get the color image
            color_image = capture.color[:, :, :3]
            color_image = np.array(color_image, dtype=np.uint8)

            # Calculate and display FPS
            if last_frame_time is not None:
                frame_fps = 1.0 / (current_time - last_frame_time)
                cv2.putText(color_image, f"FPS: {frame_fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

            # Display current focus value
            cv2.putText(color_image, f"Focus: {current_focus}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)

            last_frame_time = current_time

            cv2.namedWindow('Azure Kinect - Focus Control', cv2.WINDOW_NORMAL)
            cv2.imshow('Azure Kinect - Focus Control', color_image)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                break
            elif key == ord('a'):
                # Auto focus
                set_focus_mode(k4a, None)
                print("Switched to AUTO focus")
            elif key == ord('f'):
                # Manual focus - far
                current_focus = 800
                set_focus_mode(k4a, current_focus)
            elif key == ord('n'):
                # Manual focus - near
                current_focus = 200
                set_focus_mode(k4a, current_focus)
            elif key == ord('+') or key == ord('='):
                # Increase focus
                current_focus = min(1000, current_focus + focus_step)
                set_focus_mode(k4a, current_focus)
            elif key == ord('-'):
                # Decrease focus
                current_focus = max(0, current_focus - focus_step)
                set_focus_mode(k4a, current_focus)
            elif key == ord('r'):
                # Reset to default
                current_focus = 500
                set_focus_mode(k4a, current_focus)
            elif key == ord('i'):
                # Show focus info
                focus_info = get_current_focus(k4a)
                if focus_info:
                    print(f"Current focus info: {focus_info}")

    # Final statistics
    total_time = time.time() - start_time
    final_fps = frame_count / total_time
    print(f"\nFinal Statistics: {frame_count} frames in {total_time:.2f} seconds")
    print(f"Average FPS: {final_fps:.2f}")

    # Cleanup
    cv2.destroyAllWindows()
    k4a.stop()

if __name__ == "__main__":
    main()
