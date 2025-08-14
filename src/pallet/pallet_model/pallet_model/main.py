from stable_baselines3 import PPO
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import gym
from .Pallet_RL import envs
from .Pallet_RL.envs.src import box
# from .Pallet_RL.envs import pallet_RL
# import pallet_model.Pallet_RL.envs
import os
# from Pallet_RL.envs.argument import get_args 
import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
class Box:
    # 預先定義不同箱子的尺寸
    box_dimensions = {
        1: {'length': 40, 'width': 30, 'height': 20},
        2: {'length': 30, 'width': 25, 'height': 16},
        3: {'length': 21, 'width': 11, 'height': 14},
    }

    def __init__(self, box_id):
        if box_id not in Box.box_dimensions:
            raise ValueError(f"Box ID {box_id} is not defined.")
        
        dims = Box.box_dimensions[box_id]
        self.length = dims['length']
        self.width = dims['width']
        self.height = dims['height']

    def __str__(self):
        return f"Box: {self.length} x {self.width} x {self.height}"
# box1=box(1)
# box2=box(2)
# box3=box(3)
# # 使用範例
# box = Box(2)
# print(box.length)  # 輸出: 40
# print(box)         # 輸出: Box: 40 x 25 x 20

class PalletModel(Node):
    def __init__(self):
        super().__init__('PalletModel')
        models_dir = "src/pallet/pallet_model/pallet_model/Pallet_RL/models"
        logdir = "src/pallet/BPP_ws/Pallet_RL/logs"

        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        if not os.path.exists(logdir):
            os.makedirs(logdir)

        self.env=gym.make('pallet-v0')

        # args.mode='test'
        self.episodes=1000
        load_model="06_12_267000.0"
        self.model = PPO.load(f"{models_dir}/{load_model}")
        self.obs = self.env.reset()
        # self.srv = self.create_service(Maincontroller, 'Pallet', self.add_three_ints_callback)        # CHANGE
        self.box_type_subscriber = self.create_subscription(Int64, '/Pallet/boxtype', self.type_callback, 10)
        print("done")
        self.virtual_endpose_publisher = self.create_publisher(Twist, '/Pallet/virtualendpose', 10)
        # self.box_ep_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # self.timer = self.create_timer(1/30, self.control_loop)  # 100ms 週期執行

    def type_callback(self,msg):

        if msg.data==-1:
            self.get_logger().error('box type error', once=True)
            print("reset")
            self.obs = self.env.reset()
        else:
            action = self.model.predict(self.obs)
            self.obs, reward, done, info = self.env.step((action[0],str(msg.data)))
            
            if isinstance(info, list) and len(info) > 0 and isinstance(info[0], (list, tuple)) and len(info[0]) >= 4:
                self.get_logger().info(f'xyz: {info[0]}, rxryrz: {info[1]}')
                pose = info[0]  # [x, y, z, angz]

                if info[1][2] == 0:
                    angz = float(info[1][2])
                elif info[1][2] == -1.5707963267948966:
                    angz = math.pi/2
                    self.get_logger().info('Box is not stackable, resetting environment.')
                else:
                    angz = math.pi/2  # 預設轉角

                # 發布虛擬末端位姿
                whichbox=Box(int(msg.data))
                virtual_endpose = Twist()
                virtual_endpose.linear.x = (float(pose[0])+(whichbox.width / 2) * math.sin(angz) + (whichbox.length / 2) * math.cos(angz))*10
                virtual_endpose.linear.y = (float(pose[1])+(whichbox.width / 2) * math.cos(angz) + (whichbox.length / 2) * math.sin(angz))*10
                virtual_endpose.linear.z = (float(pose[2])+(whichbox.height))*10
                virtual_endpose.angular.z = angz*180.0/math.pi
                self.get_logger().info(f'Action: {action[0]}, Box Type: {msg.data}, Virtual End Pose: {virtual_endpose}')
                self.virtual_endpose_publisher.publish(virtual_endpose)
                self.env.render()
            else:
                self.get_logger().warn(f'Invalid or empty info returned from env.step(): {info}')
                self.obs = self.env.reset()
                
                # 發布虛擬末端位姿
                virtual_endpose = Twist()
                virtual_endpose.linear.x = float(-1.0)
                virtual_endpose.linear.y = float(-1.0)
                virtual_endpose.linear.z = float(-1.0)
                virtual_endpose.angular.z = float(-1.0)
                self.get_logger().info(f'Action: {action[0]}, Box Type: {msg.data}, Virtual End Pose: {virtual_endpose}')
                self.virtual_endpose_publisher.publish(virtual_endpose)
                self.obs = self.env.reset()
def main(args=None):
    rclpy.init(args=args)
    node = PalletModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
