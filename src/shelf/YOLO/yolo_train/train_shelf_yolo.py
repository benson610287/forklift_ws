from ultralytics import YOLO

# model = YOLO("yolo11s-pose.pt")  # load a pretrained model (recommended for training)
model = YOLO("./runs/pose/shelf_detector2/weights/last.pt")

results = model.train(
    data='./shelf_data/shelf.yaml',
    epochs=200,
    imgsz=640,
    batch=8,
    device='0',  # GPU device
    name='shelf_detector',
)
