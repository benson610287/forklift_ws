import cv2

a = 529

# 指定資料夾字串（事先要確認資料夾存在）
save_dir = 'src/pallet/pallet_main/pallet_main/yolo_picture/box'

cap = cv2.VideoCapture(6)

if not cap.isOpened():
    print("無法開啟攝影機")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("讀取影像失敗")
            continue

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key & 0xFF == ord('m'):
            a += 1
            filename = f'{save_dir}/box_{a}.jpg'
            cv2.imwrite(filename, frame)
            print(f"儲存圖片：{filename}")
        elif key & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()

