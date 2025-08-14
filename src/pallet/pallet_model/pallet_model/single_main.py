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
        self.virtual_endpose_publisher = self.create_publisher(Twist, '/Pallet/Single/virtualendpose', 10)
        # self.box_start_sub = self.create_subscription(Twist, '/Pallet/Single/startpose',self.box_start_callback,10)
         # # 移動平台命令
        # self.mobile_position_publisher = self.create_publisher(PoseStamped, '/Pallet/Single/mobile_slam_topic', 10) #topic 名稱要改！！！
        # # 手臂命令
        # self.arm_pose_publisher = self.create_publisher(Twist, '/arm_control', 10)   #topic和msg 名稱要改！！！

        self.count_s=0
        self.count_s_layer=0
        self.count_m=0
        self.count_m_layer=0
        self.count_l=0
        self.count_l_layer=0
        self.subscription  # prevent unused variable warning
        self.big_box_twist = [[200.0,150.0,200.0,0.0,0.0,0.0],
                              [600.0,150.0,200.0,0.0,0.0,0.0],
                              [200.0,450.0,200.0,0.0,0.0,0.0],
                              [600.0,450.0,200.0,0.0,0.0,0.0],
                              [200.0,150.0,400.0,0.0,0.0,0.0],
                              [600.0,150.0,400.0,0.0,0.0,0.0],
                              [200.0,450.0,400.0,0.0,0.0,0.0],
                              [600.0,450.0,400.0,0.0,0.0,0.0]
                              ]
    def box_type_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)
        if msg.data == 1:
            
            # self.get_logger().info(f'stack_l_num={self.count_l}')
            # self.get_logger().info(f'stack_l_layer={self.count_l_layer}')
            # self.get_logger().info(f'stacking_l_num={self.count_l % 4}')
            virtual_endpose = Twist()
            virtual_endpose.linear.x = self.big_box_twist[self.count_l % 8][0]
            virtual_endpose.linear.y = self.big_box_twist[self.count_l % 8][1]
            virtual_endpose.linear.z = self.big_box_twist[self.count_l % 8][2]
            virtual_endpose.angular.x = self.big_box_twist[self.count_l % 8][3]
            virtual_endpose.angular.y = self.big_box_twist[self.count_l % 8][4]
            virtual_endpose.angular.z = self.big_box_twist[self.count_l % 8][5]
            self.get_logger().info(f'Virtual End Pose: {virtual_endpose}')
            self.virtual_endpose_publisher.publish(virtual_endpose)
            self.count_l += 1
            self.count_l_layer=self.count_l / 4
            pass
        elif msg.data == 2:
            self.count_m += 1
            self.count_m_layer=self.count_m / 6
            self.get_logger().info(f'stack_m_num={self.count_m}')
            self.get_logger().info(f'stack_m_layer={self.count_m_layer}')
            self.get_logger().info(f'stacking_m_num={self.count_m % 6}')
            pass
        elif msg.data == 3:
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