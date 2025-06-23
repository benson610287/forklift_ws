import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Vector3, Twist  # <--- 加入 Twist
from math import atan2

class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0.0
        self.last_error = 0.0

    def update(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return output

class PIDMecanumController(Node):
    def __init__(self):
        super().__init__('pid_mecanum_controller')

        # 初始化 PID 控制器
        self.pid_x = PID(1.0, 0.0, 0.1)      # 控制 X 對齊（對應 linear.y）
        self.pid_z = PID(1.0, 0.0, 0.1)      # 控制深度 Z（對應 linear.x）
        self.pid_yaw = PID(1.0, 0.0, 0.1)    # 控制角度 yaw（對應 angular.z）

        self.target_depth = 0.9  # meters

        self.last_time = self.get_clock().now()

        # 資料儲存
        self.center = None
        self.normal = None

        # 訂閱者
        self.create_subscription(Point, '/plane_center', self.center_callback, 10)
        self.create_subscription(Vector3, '/plane_normal', self.normal_callback, 10)

        # 改為發布 cmd_vel (Twist)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 控制 loop
        self.timer = self.create_timer(0.02, self.control_loop)  # 50Hz

    def center_callback(self, msg):
        self.center = msg

    def normal_callback(self, msg):
        self.normal = msg

    def control_loop(self):
        if self.center is None or self.normal is None:
            return

        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        self.last_time = now

        # 誤差計算
        x_error = self.center.x  # 目標應該在畫面中間 x=0
        z_error = self.target_depth - self.center.z
        yaw_error = atan2(self.normal.x, self.normal.z)

        # PID 計算
        linear_x = self.pid_z.update(z_error, dt)     # 深度對應前後移動
        linear_y = self.pid_x.update(x_error, dt)     # X 對應左右平移
        angular_z = self.pid_yaw.update(yaw_error, dt)  # Yaw 旋轉角修正

        # 發布 cmd_vel
        twist = Twist()
        twist.linear.x = linear_x     # 前後
        twist.linear.y = linear_y     # 左右
        twist.linear.z = 0.0          # 不用上下
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = angular_z   # 原地旋轉
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = PIDMecanumController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
