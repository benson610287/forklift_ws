import pyk4a
from pyk4a import Config, PyK4A
import configparser
import os

def get_camera_intrinsics():
    config = Config()
    config.color_resolution = pyk4a.ColorResolution.RES_1080P
    config.depth_mode = pyk4a.DepthMode.NFOV_UNBINNED
    config.camera_fps = pyk4a.FPS.FPS_30

    k4a = PyK4A(config)
    k4a.open()

    # Get calibration data
    calibration = k4a.calibration

    # Color camera intrinsics
    camera_matrix = calibration.get_camera_matrix(pyk4a.CalibrationType.COLOR)
    print("Color Camera Matrix:")
    print(camera_matrix)
    dist_coeffs = calibration.get_distortion_coefficients(pyk4a.CalibrationType.COLOR)
    print("\nColor distortion:")
    print(dist_coeffs)
    k4a.close()

    output_file = "./azure_camera_calibration.ini"
    config = configparser.ConfigParser()
    config['Intrinsic'] = {
        '0_0': f"{camera_matrix[0,0]:.6f}",
        '0_1': f"{camera_matrix[0,1]:.6f}",
        '0_2': f"{camera_matrix[0,2]:.6f}",
        '1_0': f"{camera_matrix[1,0]:.6f}",
        '1_1': f"{camera_matrix[1,1]:.6f}",
        '1_2': f"{camera_matrix[1,2]:.6f}"
    }
    config['Distortion'] = {
        'k1': f"{dist_coeffs[0]:.6f}",
        'k2': f"{dist_coeffs[1]:.6f}",
        't1': f"{dist_coeffs[2]:.6f}",
        't2': f"{dist_coeffs[3]:.6f}",
        'k3': f"{dist_coeffs[4]:.6f}"
    }
    # output_file = "src/shelf_pose_est/shelf_pose_est/azure_camera_calibration.ini"
    output_file = os.path.join(os.path.dirname(__file__), './test/camera_calibration.ini')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        config.write(f)



get_camera_intrinsics()
