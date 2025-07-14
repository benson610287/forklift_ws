from ultralytics import YOLO

# 載入預訓練的 YOLOv8-seg 模型
model = YOLO('yolov8s-seg.pt')

# 開始訓練
model.train(
    data='data.yaml',  # data.yaml 的完整路徑
    epochs=100,       # 訓練的總輪數
    imgsz=640,        # 輸入影像的尺寸
    batch=16,         # 每個批次的影像數量
    name='yolov8_seg_custom',  # 訓練結果的儲存資料夾名稱
    device=0          # 使用的 GPU 編號，若使用 CPU，請設為 'cpu'
)
