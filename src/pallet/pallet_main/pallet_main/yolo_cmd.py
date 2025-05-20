import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class YoloCmdNode(Node):
    def __init__(self):
        super().__init__('yolo_cmd_node')
        self.yolo_cmd_pub = self.create_publisher(Int64, '/Pallet/yolo_cmd', 10)
        self.create_timer(0.1, self.loop)
        self.sensor_flag=True
    def loop(self):
        input("start cmd")
        if self.sensor_flag:
            msg=Int64()
            msg.data=0
            self.yolo_cmd_pub.publish(msg)
        else:
            pass

def main(args=None):
    rclpy.init(args=args)
    node = YoloCmdNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()