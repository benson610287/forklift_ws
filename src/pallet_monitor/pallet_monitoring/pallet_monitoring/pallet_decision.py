import rclpy
from rclpy.node import Node
from interfaces.msg import ClutterEvaluationArray, PalletAction, PalletMonitoringResult

class PalletDecisionNode(Node):
    def __init__(self):
        super().__init__('pallet_decision')

        self.sub_eval = self.create_subscription(
            ClutterEvaluationArray,
            'clutter_evaluations',
            self.evaluation_callback,
            10
        )

        self.pub_result = self.create_publisher(
            PalletMonitoringResult,
            'result',
            10
        )

        self.get_logger().info('✅ pallet_decision initialized.')

    def evaluation_callback(self, msg):
        self.get_logger().info(f'🤖 接收到 {len(msg.evaluations)} 筆評估資料，開始決策...')

        result = PalletMonitoringResult()
        result.header = msg.header
        result.actions = []

        for eval in msg.evaluations:
            action = PalletAction()
            action.pallet_id = eval.pallet_id
            action.score = eval.clutter_score

            if eval.needs_sorting:
                action.action_type = "sort"
                action.reason = "Clutter score too high"
            elif eval.confidence < 0.75:
                action.action_type = "alert"
                action.reason = "Low confidence"
            else:
                action.action_type = "ignore"
                action.reason = "Clutter level acceptable"

            result.actions.append(action)

        self.pub_result.publish(result)
        self.get_logger().info(f"📦 決策已發佈，共 {len(result.actions)} 筆行動")

def main(args=None):
    rclpy.init(args=args)
    node = PalletDecisionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
