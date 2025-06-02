import rclpy
from rclpy.node import Node
from interfaces.msg import CroppedPalletArray, ClutterEvaluation, ClutterEvaluationArray
import random

class ClutterEvaluatorNode(Node):
    def __init__(self):
        super().__init__('pallet_clutter_evaluator')

        self.sub_pallets = self.create_subscription(
            CroppedPalletArray,
            'cropped_pallets',
            self.pallet_callback,
            10
        )

        self.pub_result = self.create_publisher(
            ClutterEvaluationArray,
            'clutter_evaluations',
            10
        )

        self.get_logger().info('✅ pallet_clutter_evaluator initialized.')

    def pallet_callback(self, msg):
        self.get_logger().info(f'🧠 評估 {len(msg.pallets)} 個裁切圖像...')

        result = ClutterEvaluationArray()
        result.header = msg.header
        result.evaluations = []

        for pallet in msg.pallets:
            clutter_score = round(random.uniform(0.0, 1.0), 2)
            needs_sorting = clutter_score > 0.6
            confidence = round(random.uniform(0.7, 0.99), 2)

            evaluation = ClutterEvaluation()
            evaluation.pallet_id = pallet.id
            evaluation.clutter_score = clutter_score
            evaluation.needs_sorting = needs_sorting
            evaluation.confidence = confidence

            result.evaluations.append(evaluation)

        self.pub_result.publish(result)
        self.get_logger().info(f'✅ 發佈混亂評估結果，共 {len(result.evaluations)} 組')

def main(args=None):
    rclpy.init(args=args)
    node = ClutterEvaluatorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
