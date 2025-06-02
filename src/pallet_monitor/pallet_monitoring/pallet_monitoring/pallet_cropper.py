import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from interfaces.msg import PalletBBoxArray, CroppedPallet, CroppedPalletArray

class PalletCropperNode(Node):
    def __init__(self):
        super().__init__('pallet_cropper')

        self.sub_image = self.create_subscription(Image, 'image', self.image_callback, 10)
        self.sub_bboxes = self.create_subscription(PalletBBoxArray, 'yolo_result', self.bbox_callback, 10)

        self.pub_cropped = self.create_publisher(CroppedPalletArray, 'cropped_pallets', 10)

        self.latest_image = None

        self.get_logger().info("✅ pallet_cropper initialized.")

    def image_callback(self, msg):
        self.latest_image = msg  # 紀錄最新影像
        self.get_logger().info("🖼️ 影像接收成功")

    def bbox_callback(self, msg):
        if self.latest_image is None:
            self.get_logger().warn("⚠️ 尚未接收到影像，無法裁切")
            return

        self.get_logger().info(f"📦 接收到 {len(msg.bboxes)} 個 bboxes，模擬裁切中...")

        out_msg = CroppedPalletArray()
        out_msg.header = msg.header
        out_msg.pallets = []

        for bbox in msg.bboxes:
            cropped = CroppedPallet()
            cropped.id = bbox.id
            cropped.cropped_image = self.latest_image  # 模擬：直接把整張圖當作裁切圖
            out_msg.pallets.append(cropped)

        self.pub_cropped.publish(out_msg)
        self.get_logger().info(f"✅ 發佈模擬裁切結果，共 {len(out_msg.pallets)} 張")

def main(args=None):
    rclpy.init(args=args)
    node = PalletCropperNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
