import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from geometry_msgs.msg import PoseStamped,Twist
class SinglePallet(Node):

    def __init__(self):
        super().__init__('SinglePallet')
        self.subscription = self.create_subscription(
            
            Int64,
            '/Pallet/SingBoxInfo',
            self.box_type_callback,
            10)
        self.box_start_sub = self.create_subscription(Twist, '/Pallet/startpose',self.box_start_callback,10)
         # # 移動平台命令
        self.mobile_position_publisher = self.create_publisher(PoseStamped, '/mobile_slam_topic', 10) #topic 名稱要改！！！
        # # 手臂命令
        self.arm_pose_publisher = self.create_publisher(Twist, '/arm_control', 10)   #topic和msg 名稱要改！！！

        self.count_s=0
        self.count_s_layer=0
        self.count_m=0
        self.count_m_layer=0
        self.count_l=0
        self.count_l_layer=0
        self.subscription  # prevent unused variable warning

    def box_type_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        if msg.data == 0:
            self.count_l += 1
            self.count_l_layer=self.count_l / 4
            self.get_logger().info(f'stack_l_num={self.count_l}')
            self.get_logger().info(f'stack_l_layer={self.count_l_layer}')
            self.get_logger().info(f'stacking_l_num={self.count_l % 4}')
            pass
        elif msg.data == 1:
            self.count_m += 1
            self.count_m_layer=self.count_m / 6
            self.get_logger().info(f'stack_m_num={self.count_m}')
            self.get_logger().info(f'stack_m_layer={self.count_m_layer}')
            self.get_logger().info(f'stacking_m_num={self.count_m % 6}')
            pass
        elif msg.data == 2:
            self.get_logger().warning('unknown')
            pass
        else:
            self.get_logger().warning('unknown box type')
            pass


def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = SinglePallet()

    rclpy.spin(minimal_subscriber)

    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()