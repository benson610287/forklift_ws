import cv2
import numpy as np

# 開啟攝影機
cap = cv2.VideoCapture(0)

# 假設參考物是 21 cm，在影像上長度是 420 px
REFERENCE_CM = 21.0
REFERENCE_PX = 420
scale = REFERENCE_CM / REFERENCE_PX

# 建立調整 HSV 的視窗和滑桿
def nothing(x):
    pass

cv2.namedWindow("HSV Adjust")
cv2.createTrackbar("H Low", "HSV Adjust", 18, 179, nothing)
cv2.createTrackbar("S Low", "HSV Adjust", 61, 255, nothing)
cv2.createTrackbar("V Low", "HSV Adjust", 81, 255, nothing)
cv2.createTrackbar("H High", "HSV Adjust", 30, 179, nothing)
cv2.createTrackbar("S High", "HSV Adjust", 213, 255, nothing)
cv2.createTrackbar("V High", "HSV Adjust", 233, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        print("無法讀取影像")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 讀取滑桿的 HSV 範圍
    h_low = cv2.getTrackbarPos("H Low", "HSV Adjust")
    s_low = cv2.getTrackbarPos("S Low", "HSV Adjust")
    v_low = cv2.getTrackbarPos("V Low", "HSV Adjust")
    h_high = cv2.getTrackbarPos("H High", "HSV Adjust")
    s_high = cv2.getTrackbarPos("S High", "HSV Adjust")
    v_high = cv2.getTrackbarPos("V High", "HSV Adjust")

    lower = np.array([h_low, s_low, v_low])
    upper = np.array([h_high, s_high, v_high])

    # 顏色遮罩
    mask = cv2.inRange(hsv, lower, upper)
        # --- 加入形態學處理來去雜訊 ---
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # 去小點雜訊
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel) # 填補小空洞

    blur = cv2.GaussianBlur(mask, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # 找輪廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if cv2.contourArea(cnt) < 1000:
            continue  # 忽略小雜點
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        if len(approx) == 4 and cv2.contourArea(cnt) > 1000:
            box_pts = approx.reshape(4, 2)
            edge1 = np.linalg.norm(box_pts[0] - box_pts[1])
            edge2 = np.linalg.norm(box_pts[1] - box_pts[2])
            width_px = min(edge1, edge2)
            height_px = max(edge1, edge2)

            width_cm = width_px * scale
            height_cm = height_px * scale

            # 畫出矩形與標籤
            cv2.drawContours(frame, [approx], -1, (0, 255, 0), 2)
            x, y = box_pts[0]
            cv2.putText(frame, f"{width_cm:.1f}cm x {height_cm:.1f}cm", (int(x), int(y)-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # 顯示畫面
    cv2.imshow("Box Detection", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
