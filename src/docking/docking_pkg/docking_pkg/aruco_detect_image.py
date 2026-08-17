import cv2
import numpy as np
import math

# ============ 使用者設定 ============ #
image_path = "aruco_sample.jpeg"   # ← 輸入你的圖片檔名
marker_length = 0.1               # Marker 實際邊長 (m)
aruco_id_to_detect = 5            # 想偵測的目標 ID
# ================================== #

# 假設的相機內參 (可依實際相機標定結果修改)
fx = 600.0
fy = 600.0
cx = 320.0
cy = 240.0
K = np.array([[fx, 0, cx],
              [0, fy, cy],
              [0,  0,  1]], dtype=np.float64)
D = np.zeros((5,))  # 無畸變假設

# 建立 ArUco 字典與偵測器
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector_params = cv2.aruco.DetectorParameters()
aruco_detector = cv2.aruco.ArucoDetector(aruco_dict, detector_params)

# 讀取影像
frame = cv2.imread(image_path)
if frame is None:
    raise FileNotFoundError(f"找不到圖片檔案：{image_path}")

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# 偵測 ArUco
corners, ids, rejected = aruco_detector.detectMarkers(gray)

if ids is None or len(ids) == 0:
    print("❌ 沒有偵測到任何 ArUco Marker")
else:
    cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    print(f"✅ 偵測到 {len(ids)} 個 Marker：{ids.flatten()}")

    for i, marker_id in enumerate(ids.flatten()):
        if marker_id == aruco_id_to_detect:
            # 取得該 marker 的四個角點
            corner_points = corners[i][0].astype(np.float32)

            # ArUco Marker 在世界座標系中的四個角點（以中心為原點）
            half_len = marker_length / 2
            obj_points = np.array([
                [-half_len,  half_len, 0],
                [ half_len,  half_len, 0],
                [ half_len, -half_len, 0],
                [-half_len, -half_len, 0]
            ], dtype=np.float32)

            # 使用 solvePnP 估算姿態
            success, rvec, tvec = cv2.solvePnP(
                obj_points, corner_points, K, D, flags=cv2.SOLVEPNP_IPPE_SQUARE
            )

            if success:
                cv2.drawFrameAxes(frame, K, D, rvec, tvec, 0.05)

                x, y, z = tvec.flatten()
                rx, ry, rz = rvec.flatten()
                rz_deg = math.degrees(rz)

                print(f"--- Marker ID {marker_id} ---")
                print(f"位置 (x, y, z): {x:.3f}, {y:.3f}, {z:.3f} m")
                print(f"旋轉角度 (rx, ry, rz): {math.degrees(rx):.2f}, {math.degrees(ry):.2f}, {rz_deg:.2f} 度")
                print("----------------------------------")

# 顯示結果
cv2.imshow("Aruco Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
