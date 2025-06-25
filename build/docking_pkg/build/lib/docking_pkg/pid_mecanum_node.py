import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Vector3, Twist
from math import atan2, pi

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

    def reset(self):
        self.integral = 0.0
        self.last_error = 0.0

class PIDMecanumController(Node):
    def __init__(self):
        super().__init__('pid_mecanum_controller')

        # 初始化 PID 控制器
        self.pid_x = PID(1.0, 0.0, 0.1)      # 控制畫面中心 X 對齊（linear.y）
        self.pid_z = PID(1.0, 0.0, 0.1)      # 控制深度（linear.x）
        self.pid_yaw = PID(1.0, 0.0, 0.1)    # 控制法向量角度（angular.z）

        self.target_depth = 1.0  # 目標深度（公尺）

        self.last_time = self.get_clock().now()

        # 接收的資料
        self.center = None
        self.normal = None

        # 訂閱主題
        self.create_subscription(Point, '/plane_center', self.center_callback, 10)
        self.create_subscription(Vector3, '/plane_normal', self.normal_callback, 10)

        # 發布 /cmd_vel
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        # 啟動控制迴圈（50Hz）
        self.timer = self.create_timer(0.02, self.control_loop)

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
        x_error = self.center.x
        z_error = self.target_depth - self.center.z
        yaw_error = atan2(self.normal.x, self.normal.z)

        # 修正：如果角度大於 ±90 度，代表背對鏡頭，轉換為最近旋轉方向
        if abs(yaw_error) > pi / 2:
            yaw_error = yaw_error - pi if yaw_error > 0 else yaw_error + pi

        # 死區處理：小於 ±5 度則視為對準
        if abs(yaw_error) < 0.0873:
            angular_z = 0.0
            self.pid_yaw.reset()
        else:
            angular_z = self.pid_yaw.update(yaw_error, dt)

        # 計算 linear 控制輸出
        linear_x = self.pid_z.update(z_error, dt)
        linear_y = self.pid_x.update(x_error, dt)

        # 發布 Twist 指令
        twist = Twist()
        twist.linear.x = linear_x
        twist.linear.y = linear_y
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = angular_z
        self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = PIDMecanumController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
