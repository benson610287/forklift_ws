import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Vector3, Twist
from std_msgs.msg import Int64
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

        self.pid_x = PID(1.0, 0.0, 0.1)
        self.pid_z = PID(1.0, 0.0, 0.1)
        self.pid_yaw = PID(1.0, 0.0, 0.1)

        self.target_depth = 1.0
        self.last_time = self.get_clock().now()

        self.center = None
        self.normal = None
        self.center_time = None
        self.normal_time = None
        self.timeout_sec = 0.5

        self.success_counter = 0
        self.required_success = 20

        self.task_done = False
        self.movement_phase = 'yaw_pid'  # 🚀 初始進入角度控制階段
        self.phase_start_time = None

        self.create_subscription(Point, '/plane_center', self.center_callback, 10)
        self.create_subscription(Vector3, '/plane_normal', self.normal_callback, 10)

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.docking_pub = self.create_publisher(Int64, '/dockingfinish', 10)

        self.timer = self.create_timer(0.02, self.control_loop)


        self.count=0


    def center_callback(self, msg):
        self.center = msg
        self.center_time = self.get_clock().now()

    def normal_callback(self, msg):
        self.normal = msg
        self.normal_time = self.get_clock().now()

    def control_loop(self):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9
        self.last_time = now
        
        # 檢查資料是否過期
        if (self.center_time is None or self.normal_time is None
            # (now - self.center_time).nanoseconds / 1e9 > self.timeout_sec or
            # (now - self.normal_time).nanoseconds / 1e9 > self.timeout_sec
            ):
            self.get_logger().warn('Missing or stale /plane_center or /plane_normal data. Sending zero velocity.')
            # self.publish_zero_twist()
            return

        # 計算誤差
        x_error = self.center.x - 0.07
        z_error = self.target_depth - self.center.z
        yaw_error = atan2(self.normal.x, self.normal.z)
        if abs(yaw_error) > pi / 2:
            yaw_error = yaw_error - pi if yaw_error > 0 else yaw_error + pi

        # === Phase 1: Yaw PID Control ===
        if self.movement_phase == 'yaw_pid':
            angular_z = self.pid_yaw.update(yaw_error, dt) / -80
            twist = Twist()
            twist.angular.z = angular_z
            self.cmd_pub.publish(twist)

            if abs(yaw_error) < 0.0373:
                self.success_counter += 1
                self.publish_zero_twist()
                self.get_logger().info(f"[Yaw PID] Alignment success count: {self.success_counter}/{self.required_success}")
            else:
                self.success_counter = 0

            if self.success_counter >= self.required_success:
                self.get_logger().info("Yaw alignment done → switching to XZ PID phase.")
                self.success_counter = 0
                self.pid_yaw.reset()
                self.movement_phase = 'xz_pid'
                return
            return

        # === Phase 2: XZ PID Control ===
        if self.movement_phase == 'xz_pid':
            # 若角度偏差太大則回去修正角度
            if abs(yaw_error) > 0.1:
                self.get_logger().warn("Yaw drift detected, switching back to yaw_pid.")
                self.movement_phase = 'yaw_pid'
                return

            # 控制X與Z
            linear_x = self.pid_z.update(z_error, dt) / -80
            linear_y = self.pid_x.update(x_error, dt) / -80
            # angular_z = self.pid_yaw.update(yaw_error, dt) / -10

            twist = Twist()
            twist.linear.x = linear_x
            twist.linear.y = linear_y
            # twist.angular.z = angular_z
            self.cmd_pub.publish(twist)

            aligned = (abs(x_error) < 0.05 and abs(z_error) < 0.05 and abs(yaw_error) < 0.045)
            if aligned:
                self.success_counter += 1
                self.get_logger().info(f"[XZ PID] Alignment success count: {self.success_counter}/{self.required_success}")
            else:
                self.success_counter = 0

            if self.success_counter >= self.required_success and not self.task_done:
                self.get_logger().info("Docking alignment confirmed. Enter waiting phase.")
                self.publish_zero_twist()
                self.task_done = True
                self.movement_phase = 'waiting'
                self.phase_start_time = now
                return
            return

        # === Phase 3: Waiting ===
        if self.movement_phase == 'waiting':
            if (now - self.phase_start_time).nanoseconds / 1e9 >= 5.0:
                self.get_logger().info('Waiting done. Start moving forward.')
                self.phase_start_time = now
                self.movement_phase = 'forwarding'
            else:
                self.publish_zero_twist()
            
            
            return

        # === Phase 4: Forwarding ===
        elif self.movement_phase == 'forwarding':
            if (now - self.phase_start_time).nanoseconds / 1e9 >= 10.5:
                self.get_logger().info('Forwarding done. Stop and publish dockingfinish.')
                self.publish_zero_twist()
                self.docking_pub.publish(Int64(data=1))
                self.movement_phase = 'done'
            else:
                twist = Twist()
                twist.linear.x = 0.1  # Move forward at 0.1 m/s
                self.cmd_pub.publish(twist)
            return

        elif self.movement_phase == 'done':
            if self.count<=10:
                self.publish_zero_twist()
                self.count+=1
            else:
                self.movement_phase=None
                print("=====================")
                # self.de
            # self.destroy_node()
            # rclpy.shutdown()
            
            return

    def publish_zero_twist(self):
        self.cmd_pub.publish(Twist())


def main(args=None):
    rclpy.init(args=args)
    node = PIDMecanumController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
