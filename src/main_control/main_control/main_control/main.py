from interface.srv import Maincontroller
from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node

from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time
class controller(Node):

    def __init__(self):
        super().__init__('MainControl')
        client_group1=ReentrantCallbackGroup()
        server_group=client_group1




        self.srv = self.create_service(Taskcmd, 'taskcmd', self.aa,callback_group=server_group)

        self.cli_pallet = self.create_client(Maincontroller, 'Pallet',callback_group=client_group1)
        while not self.cli_pallet.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        self.cli_shelf_pose = self.create_client(Maincontroller, 'toggle_aruco_detection',callback_group=client_group1)
        while not self.cli_shelf_pose.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        # self.cli_3 = self.create_client(Maincontroller, 'add_two_ints')
        # while not self.cli_3.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        
        # self.cli_4 = self.create_client(Maincontroller, 'add_two_ints')
        # while not self.cli_4.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        
        # self.cli_5 = self.create_client(Maincontroller, 'add_two_ints')
        # while not self.cli_5.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        self.req = Maincontroller.Request()

    async def aa(self,req,res):
        if req.task=="task1":
            self.get_logger().info("Calling Pallet...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            future = self.cli_pallet.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("inner_res.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"Inner service failed: {e}")
                res.state = -1
            
        elif req.task=="task2_start":
            self.get_logger().info("starting shelf_pose...")
            inner_req = Maincontroller.Request()
            inner_req.enable = True
            future = self.cli_shelf_pose.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("inner_res.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"Inner service failed: {e}")
                res.state = -1


        elif req.task=="task2_close":
            self.get_logger().info("closing shelf_pose...")
            inner_req = Maincontroller.Request()
            inner_req.enable = False
            future = self.cli_shelf_pose.call_async(inner_req)
            while not future.done():
                time.sleep(0.01)
            try:
                inner_res = future.result()
                print("inner_res.done=",inner_res.done)
                res.state=inner_res.done
            except Exception as e:
                self.get_logger().error(f"Inner service failed: {e}")
                res.state = -1


        elif req.task=="task3":
            print("a")
            # self.req.enable=True
            # self.future = self.cli_3.call_async(self.req)
            # rclpy.spin_until_future_complete(self, self.future)
            # res=self.future.result()
            # print(res.done)
            res.state=3
        elif req.task=="task4":
            print("a")
            # self.req.enable=True
            # self.future = self.cli_4.call_async(self.req)
            # rclpy.spin_until_future_complete(self, self.future)
            # res=self.future.result()
            # print(res.done)
            res.state=4
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


    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    minimal_client = controller()
    executor=MultiThreadedExecutor()
    executor.add_node(minimal_client)
    minimal_client.get_logger().info('beginning')
    executor.spin()
    # response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    # minimal_client.get_logger().info(
    #     'Result of add_two_ints: for %d + %d = %d' %
    #     (int(sys.argv[1]), int(sys.argv[2]), response.sum))
    # rclpy.spin(minimal_client)
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()