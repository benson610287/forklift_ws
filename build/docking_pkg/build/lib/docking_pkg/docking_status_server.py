from interface.srv import Maincontroller  # 假設 .srv 檔叫 TaskStatus.srv
import rclpy
from rclpy.node import Node
import time
import random  # 用來模擬成功/失敗的狀況


class DockingStatusServer(Node):

    def __init__(self):
        super().__init__('docking_status_server')
        self.srv = self.create_service(Maincontroller, 'docking_status_server', self.docking_status_callback)
        self.get_logger().info('DockingTaskStatus service is ready.')

    def docking_status_callback(self, request, response):
        self.get_logger().info(f'Received task request. run = {request.run}')

        if request.run:
            self.get_logger().info('Task started...')
            time.sleep(3)  # 模擬任務執行時間

            # 模擬任務是否成功（你可以改成真實判斷）
            success = random.choice([True, False])

            if success:
                self.get_logger().info('Task completed successfully.')
                response.state = 0
            else:
                self.get_logger().warn('Task failed or interrupted!')
                response.state = 1
        else:
            self.get_logger().info('Task not started. run=False')
            response.state = 1

        return response


def main(args=None):
    rclpy.init(args=args)
    node = DockingStatusServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
