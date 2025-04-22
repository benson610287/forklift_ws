import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from interface.srv import Maincontroller     # CHANGE
import math
import random
class TurtlePControl(Node):
    def __init__(self):
        super().__init__('PalletMain')
        self.srv = self.create_service(Maincontroller, 'Pallet', self.add_three_ints_callback)        # CHANGE
        # # 訂閱烏龜的位置信息
        # self.pose_subscriber = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)

        # # 發布速度指令
        # self.velocity_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # self.timer = self.create_timer(1/30, self.control_loop)  # 100ms 週期執行

    def add_three_ints_callback(self, request, response):
        if request.enable==True:
            response.done = 1                                                  # CHANGE
        else:
            response.done = 2
        self.get_logger().info('Incoming request\na: %d' % (response.done)) # CHANGE

        return response
    # def pose_callback(self, msg):
    #     """更新烏龜的當前位姿"""
    #     self.pose = msg

    def control_loop(self):
        pass
        # cmd_vel=Twist()
        # self.velocity_publisher.publish(cmd_vel)
        #     # 發佈速度：依照 P 控制所計算的線速度


        #     # 顯示當前狀態
        # self.get_logger().info(f'距離目標: {cmd_vel:.2f}, 設定線速度: {cmd_vel:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = TurtlePControl()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()