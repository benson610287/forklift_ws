from interface.srv import Maincontroller
from gui_interface.srv import Taskcmd
import rclpy
from rclpy.node import Node
from pallet_interfaces.srv import Palletstate

class controller(Node):

    def __init__(self):
        super().__init__('MainControl')

        self.srv = self.create_service(Taskcmd, 'taskcmd', self.aa)

        self.cli_1 = self.create_client(Palletstate, 'Palletstate')
        while not self.cli_1.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        
        # self.cli_2 = self.create_client(Maincontroller, 'add_two_ints')
        # while not self.cli_2.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('service not available, waiting again...')
        
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

    def aa(self,req,res):
        if req.task=="task1":
            print("a")
            self.req.enable=True
            self.future = self.cli_1.call_async(self.req)
            rclpy.spin_until_future_complete(self, self.future)
            res=self.future.result()
            print(res.done)
            res.state=1
        elif req.task=="task2":
            print("a")
            # self.req.enable=True
            # self.future = self.cli_2.call_async(self.req)
            # rclpy.spin_until_future_complete(self, self.future)
            # res=self.future.result()
            # print(res.done)
            res.state=2
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
    # response = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    # minimal_client.get_logger().info(
    #     'Result of add_two_ints: for %d + %d = %d' %
    #     (int(sys.argv[1]), int(sys.argv[2]), response.sum))
    rclpy.spin(minimal_client)
    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()