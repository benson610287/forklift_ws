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
        # # 訂閱烏龜的位置信息
        self.box_type_subscriber = self.create_subscription(Int64, '/Pallet/boxtype', self.type_callback, 10)
        print("done")
        # # 發布速度指令
        # self.box_ep_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        # self.timer = self.create_timer(1/30, self.control_loop)  # 100ms 週期執行

    def type_callback(self,msg):


        action = self.model.predict(self.obs)
        self.obs, reward, done, info = self.env.step((action[0],str(msg.data)))
        print("action=",action[0],"stack_ep=",info[0])
        self.env.render()
        # input("aaaaa=")
        
        # self.env.close()

        pass




def main(args=None):
    rclpy.init(args=args)
    node = PalletModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()