import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from interfaces.msg import PalletBBox, PalletBBoxArray

class PalletYoloDetector(Node):
    def __init__(self):
        super().__init__('pallet_yolo_detector')

        self.subscription = self.create_subscription(
            Image,
            'image',
            self.image_callback,
            10
        )

        self.publisher = self.create_publisher(
            PalletBBoxArray,
            'yolo_result',
            10
        )

        self.get_logger().info('✅ pallet_yolo_detector initialized.')

    def image_callback(self, msg):
        self.get_logger().info('📷 Image received. Publishing fake YOLO results...')

        # 模擬兩個bbox
        bbox1 = PalletBBox()
        bbox1.id = 0
        bbox1.x_min = 100.0
        bbox1.y_min = 150.0
        bbox1.x_max = 300.0
        bbox1.y_max = 400.0
        bbox1.confidence = 0.9
        bbox1.class_label = "pallet"

        bbox2 = PalletBBox()
        bbox2.id = 1
        bbox2.x_min = 350.0
        bbox2.y_min = 100.0
        bbox2.x_max = 550.0
        bbox2.y_max = 350.0
        bbox2.confidence = 0.85
        bbox2.class_label = "pallet"

        result_msg = PalletBBoxArray()
        result_msg.header = msg.header
        result_msg.bboxes = [bbox1, bbox2]

        self.publisher.publish(result_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PalletYoloDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
