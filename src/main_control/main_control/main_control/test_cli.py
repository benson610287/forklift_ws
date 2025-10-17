import sys


import rclpy
from rclpy.node import Node
from gui_interface.srv import Taskcmd
from threading import Event
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(Taskcmd, 'taskcmd')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = Taskcmd.Request()
        self.tasklist_first=["slam_parking","parking","palleting"]
        # self.tasklist_first=["slam_parking","parking","palleting","slam_goto_docking","slam_pre_docking","docking","start_positioning","shelf_docking","close_positioning","slam_home"]
        self.tasklist_second=["start_positioning","shelf_docking","close_positioning","slam_home"]


        # self.tasklist=["slam_pre_docking", "docking", "start_positioning", "shelf_docking", "close_positioning", "slam_home"]
        # self.tasklist=["start_positioning", "shelf_docking", "close_positioning", "slam_home"]
        # self.tasklist=["slam_pre_docking", "docking", "start_positioning", "shelf_docking", "close_positioning", "slam_home"]
        # self.tasklist=["slam_parking","parking","slam_goto_docking","slam_pre_docking","docking","start_positioning","shelf_docking","close_positioning","slam_home"]
        self.event=Event()


    def send_request(self):
        while len(self.tasklist_first)>=1:
        # while len(self.tasklist_second)>=1:
            self.req.task=self.tasklist_first.pop(0)
            # self.req.task=self.tasklist_second.pop(0)
            self.get_logger().info(f'doing {self.req.task}  plese wait')
            self.future = self.cli.call_async(self.req)
            # self.future.add_done_callback(self.client_callback)
            # self.ressss = self.cli.call(self.req)

            rclpy.spin_until_future_complete(self, self.future)
            # self.event.wait()
            # self.event.clear()
            self.get_logger().info(f'{self.req.task} is done plese check')
            
        return 0

    def client_callback(self, future):
        try:
            # self.res = future.result()
            self.event.set()
            self.get_logger().info(f'{self.req.task} is done plese check')
        except Exception as e:
            self.get_logger().error(f'move service call failed: {e}')
def main():
    rclpy.init()

    minimal_client = MinimalClientAsync()
    minimal_client.send_request()

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()