from interface.srv import Maincontroller
from interface.msg import ShelfState
from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time

from std_msgs.msg import Float32MultiArray , Int32

class controller(Node):

    def __init__(self):
        super().__init__('MainControl')
        client_group1=ReentrantCallbackGroup()
        server_group=client_group1
        


        self.srv = self.create_service(Taskcmd, 'taskcmd', self.aa, callback_group=server_group)

        self.pallet = self.create_client(Maincontroller, 'Pallet',callback_group=client_group1)
        # while not self.cli_pallet.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('pallet service not available, waiting again...')
        
        self.shelf_pose = self.create_client(Maincontroller, 'toggle_aruco_detection',callback_group=client_group1)
        # while not self.cli_shelf_pose.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('shelf_pose service not available, waiting again...')

        self.docking = self.create_client(Maincontroller, 'docking_status_server',callback_group=client_group1)  #docking
        # while not self.cli_docking.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('docking service not available, waiting again...')
        
        self.shelf_docking = self.create_client(Maincontroller, 'shelf_docking',callback_group=client_group1)
        # while not self.cli_4.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        
        # self.cli_5 = self.create_client(Maincontroller, 'add_two_ints',callback_group=client_group1)
        # while not self.cli_5.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        self.slam_pub = self.create_publisher(Float32MultiArray, '/timda_nav_pose', 10)
        self.slam_sub = self.create_subscription(
            Int32,
            '/timda_nav_success',
            self.slam_callback,
            10)


        

        self.check_client_list=[
            # self.pallet,
            # self.shelf_pose,
            # self.docking,
        ]

        for i in self.check_client_list:
            while not i.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(i.srv_name +' server not available, waiting again...')



        self.slam_flag=False
        self.home_flag=True
        self.pallet_mode='mix'
        self.req = Maincontroller.Request()


    def slam_callback(self,msg):
        if msg.data==1:
            self.slam_flag=False
        else:
            self.slam_flag=True
        pass

    async def aa(self,req,res):
        if req.task=="palleting":
            self.get_logger().info("Calling palleting...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            future = self.pallet.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("palleting_inner_res.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"palleting Inner service failed: {e}")
                res.state = -1
            
        elif req.task=="start_positioning":
            self.get_logger().info("starting positioning...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            future = self.shelf_pose.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("start_positioning.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"start_positioning Inner service failed: {e}")
                res.state = -1


        elif req.task=="close_positioning":
            self.get_logger().info("closing positioning...")
            inner_req = Maincontroller.Request()
            inner_req.enable = False
            future = self.shelf_pose.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("close_positioning.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"close_positioning Inner service failed: {e}")
                res.state = -1


        elif req.task=="docking":
            self.get_logger().info("starting docking...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            future = self.docking.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("docking_inner_res.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"docking Inner service failed: {e}")
                res.state = -1

        elif req.task=="shelf_docking":
            self.get_logger().info("starting shelf_docking...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            future = self.shelf_docking.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("shelf_docking_inner_res.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"shelf_docking Inner service failed: {e}")
                res.state = -1

        elif req.task=="task5":
            print("a")
            # self.req.enable=True
            # self.future = self.cli_5.call_async(self.req)
            # rclpy.spin_until_future_complete(self, self.future)
            # res=self.future.result()
            # print(res.done)
            res.state=5
        elif req.task=="task6":
            print("a")
            # self.req.enable=True
            # self.future = self.cli_6.call_async(self.req)
            # rclpy.spin_until_future_complete(self, self.future)
            # res=self.future.result()
            # print(res.done)
            res.state=6
        return res




def main(args=None):
    rclpy.init(args=args)

    minimal_client = controller()
    executor=MultiThreadedExecutor()
    executor.add_node(minimal_client)
    minimal_client.get_logger().info('beginning')
    executor.spin()

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()