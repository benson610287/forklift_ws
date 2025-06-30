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


import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist
class PalletModel(Node):
    def __init__(self):
        super().__init__('PalletModel')
        models_dir = "src/pallet/BPP_ws/Pallet_RL/models"
        logdir = "src/pallet/BPP_ws/Pallet_RL/logs"

        if not os.path.exists(models_dir):
            os.makedirs(models_dir)

        if not os.path.exists(logdir):
            os.makedirs(logdir)

        self.env=gym.make('pallet-v0')

        # args.mode='test'
        self.episodes=1000
        load_model="11_04_400000.0"
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
            self.get_logger().info(f'Action: {action[0]}, Box Type: {msg.data}, Stack EP: {info[0]}')
            if info[0][3] == 0:
                angz= info[0][3]
            elif info[0][3] == -50:
                angz = 1.57
                self.get_logger().info('Box is not stackable, resetting environment.')
            # 發布虛擬末端位姿
            virtual_endpose = Twist()
            virtual_endpose.linear.x = info[0][0]
            virtual_endpose.linear.y = info[0][1]
            virtual_endpose.linear.z = info[0][2]
            virtual_endpose.angular.z = angz
            self.get_logger().info(f'Virtual End Pose: {virtual_endpose}')
            self.virtual_endpose_publisher.publish(virtual_endpose)

            self.env.render()
def main(args=None):
    rclpy.init(args=args)
    node = PalletModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()