from ultralytics import YOLO
import cv2
# Load a COCO-pretrained YOLOv8n model
model = YOLO("src/pallet/pallet_main/pallet_main/box.v7i.yolov8-obb/yolov8m-obb.pt")

# Display model information (optional)
model.info()

# Train the model on the COCO8 example dataset for 100 epochs
results = model.train(data="src/pallet/pallet_main/pallet_main/box.v7i.yolov8-obb/data.yaml", epochs=10000, imgsz=640)

# Run inference with the YOLOv8n model on the 'bus.jpg' image
# results = model("src/pallet/pallet_main/pallet_main/Screenshot from 2025-03-26 15-42-50.png")
