import pyrealsense2 as rs
from ultralytics import YOLO
import numpy as np
import cv2

# # Load a pretrained YOLO11n model
# model = YOLO("yolo12n.pt")
# model.export(format="engine")
tensorrt_model = YOLO("yolo12n.engine")

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)
pipeline.start(config)

while 1:
    frame = pipeline.wait_for_frames()
    color_frame = frame.get_color_frame()
    image_mat = np.asanyarray(color_frame.get_data())

    if image_mat is not None:
        results = tensorrt_model(image_mat)
        annotated_frame = results[0].plot()

        cv2.imshow('YOLO inference',annotated_frame)
        cv2.setWindowProperty('YOLO inference',
                            cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_NORMAL)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        print("No camera frames")
        break

pipeline.stop()
cv2.destroyAllWindows()
