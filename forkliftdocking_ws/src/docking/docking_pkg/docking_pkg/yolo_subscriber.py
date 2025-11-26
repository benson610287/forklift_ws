import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
import numpy as np
import os

class YoloSubscriber(Node):
    def __init__(self):
        super().__init__('yolo_subscriber')
        
        # 訂閱影像
        self.subscription = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.listener_callback,10)
        
        self.bridge = CvBridge()

        # 載入YOLO模型（可換成 yolov8s.pt 等）
        # model_path = os.path.join(os.path.dirname(__file__), 'yolov8_models', 'best.pt')

        model_path = '/home/flash/work/src/docking/docking_pkg/yolov8_models/last.pt'


        self.model = YOLO(model_path)
        self.get_logger().info('YOLOv8 node initialized.')

    def listener_callback(self, msg):
        try:
            # ROS影像轉OpenCV影像
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # 推論
            results = self.model(frame)

            # 畫上辨識結果
            annotated_frame = results[0].plot()

            # 顯示畫面（除錯用）
            cv2.imshow("YOLOv8 Detection", annotated_frame)
            cv2.waitKey(1)

        except Exception as e:
            self.get_logger().error(f"Error in YOLO callback: {str(e)}")

def main(args=None):
    rclpy.init(args=args)
    node = YoloSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
