from interface.srv import Maincontroller  # .srv 檔案
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from std_msgs.msg import Int64

class DockingStatusServer(Node):

    def __init__(self):
        super().__init__('docking_status_server')
        self.srv = self.create_service(Maincontroller, 'docking_status_server', self.docking_status_callback)
        self.publisher_ = self.create_publisher(Bool, 'dockingstart', 10)
        self.subscriber_ = self.create_subscription(Int64, 'dockingfinish', self.finish_callback, 10)

        self.docking_done = None  # 用來儲存 dockingfinish 的結果
        self.get_logger().info('DockingStatusServer is ready.')

    def finish_callback(self, msg):
        self.get_logger().info(f'Received dockingfinish: {msg.data}')
        self.docking_done = msg.data  # 儲存 finish 狀態

    def docking_status_callback(self, request, response):
        self.get_logger().info(f'Received service request: enable = {request.enable}')

        if request.enable:
            self.get_logger().info('Publishing dockingstart=True...')
            self.publisher_.publish(Bool(data=True))

            # 等待 dockingfinish 資料
            self.docking_done = None
            timeout = self.get_clock().now().seconds_nanoseconds()[0] + 50  # 最多等 10 秒

            while rclpy.ok():
                if self.docking_done is not None:
                    response.done = self.docking_done
                    self.publisher_.publish(Bool(data=False))

                    self.get_logger().info(f'Responding with done = {response.done}')
                    break
                if self.get_clock().now().seconds_nanoseconds()[0] > timeout:
                    self.get_logger().warn('Timeout waiting for dockingfinish')
                    response.done = -1  # 超時
                    self.publisher_.publish(Bool(data=False))
                    break
                rclpy.spin_once(self, timeout_sec=0.1)
        else:
            self.get_logger().info('enable is False, skipping docking.')
            response.done = -1
            self.publisher_.publish(Bool(data=False))

        return response


def main(args=None):
    rclpy.init(args=args)
    node = DockingStatusServer()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
