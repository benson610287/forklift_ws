import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseArray, Twist
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int64
from interface.srv import Maincontroller
from interface.msg import ShelfState

from enum import Enum
from cv_bridge import CvBridge
import os
import configparser
import numpy as np
from scipy.spatial.transform import Rotation as R
import time


class States(Enum):
    CAMERA_POSE = 0
    LOCK_SHELF_STATE = 1
    MOVE_CAR = 2
    SHELF_DOCKING = 3
    DONE = 4 
    YAW_CONTROL = 5
    X_CONTROL = 6
    MOVE_IN = 7
    MOVE_DOWN = 8
    MOVE_OUT = 9
    SEARCH_MARKER = 10

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

class ShelfDockingNode(Node):
    def __init__(self):
        super().__init__('shelf_docking_node')
        self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 10)
        # self.service = self.create_service(Maincontroller, 'shelf_docking', self.service_callback)
        self.linear_motor_publisher = self.create_publisher(Int64, '/topic', 10)
        self.mecanum_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.shelf_state_subscriber = self.create_subscription(ShelfState, '/shelf/state', self.shelf_callback, 10)
        
        # self.linear_motor_timer = self.create_timer(1.0, self.publish_linear_motor)
        linear_msg = Int64()
        linear_msg.data = 98
        self.linear_motor_publisher.publish(linear_msg)

        self.active = False
        self.max_coontrol_vel = 0.2
        self.z_target = 1.45 #1.45 meters away from marker
        self.x_left_target = 0.07
        self.x_right_target = -0.64
        self.move_in = None
        self.move_out = None
        self.STATE = States.YAW_CONTROL

        self.move_start_time = None
        dis_const = 85
        self.wheel_speed = 0.1
        self.move_duration = dis_const * self.wheel_speed

    # def service_callback(self, request, response):
    #     if request.enable and not self.active:
    #         self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 10)
    #         self.linear_motor_publisher = self.create_publisher(Int64, '/topic', 10)
    #         self.mecanum_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
    #         self.shelf_state_subscriber = self.create_subscription(ShelfState, '/shelf/state', self.shelf_callback, 10)
    #         self.active = True
    
    #     elif not request.enable and self.active:
    #         self.destroy_subscription(self.shelf_pose_subscriber)
    #         self.destroy_publisher(self.linear_motor_publisher)
    #         self.destroy_publisher(self.mecanum_publisher)
    #         self.active = False

    def shelf_callback(self, msg):
        shelf_state = msg

    def publish_linear_motor(self):
        linear_msg = Int64()

        if self.STATE == States.YAW_CONTROL or self.STATE == States.X_CONTROL or self.STATE == States.MOVE_IN:
            linear_msg.data = 30
            self.linear_motor_publisher.publish(linear_msg)
            self.get_logger().info(f"Linear Motor:{linear_msg.data} (State: {self.STATE.name})")

        elif self.STATE == States.MOVE_DOWN:
            linear_msg.data = 20
            self.linear_motor_publisher.publish(linear_msg)
            time.sleep(3.0)
            self.move_start_time = self.get_clock().now()
            self.STATE = States.MOVE_OUT 
        
        elif self.STATE == States.MOVE_OUT:
            linear_msg.data = 20
            self.linear_motor_publisher.publish(linear_msg)

        elif self.STATE == States.DONE:
            linear_msg.data = 0
            self.linear_motor_publisher.publish(linear_msg)
            self.get_logger().info(f"Linear motor stopped: {linear_msg.data}")
        else:
            linear_msg.data = 0
            self.linear_motor_publisher.publish(linear_msg)

    def pose_callback(self, msg):
        pose = msg.poses[1]
        if any([pose.position.x, pose.position.y, pose.position.z]):
            pass
        else:
            pose = msg.poses[3]
            if any([pose.position.x, pose.position.y, pose.position.z]):
                pass
            else:
                self.STATE = States.SEARCH_MARKER

        
        quat = [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]
        r = R.from_quat(quat)
        euler_angles = r.as_euler('xyz', degrees=True)
        yaw_error = euler_angles[1]

        z_value = pose.position.z
        z_error = z_value - self.z_target

        x_value = pose.position.x
        x_error = self.x_right_target - x_value

        twist_msg = Twist()

        if self.STATE == States.YAW_CONTROL:

            if abs(yaw_error) >= 0.3 or abs(z_error) >= 0.03:
                self.get_logger().info("YAW Z Alignment")
                yaw_control = -(yaw_error * 0.001)

                z_control = z_error * 0.3
                twist_msg.linear.x = float(z_control)
                twist_msg.linear.x = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.linear.x))

                twist_msg.angular.z = float(yaw_control)
                twist_msg.angular.z = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.angular.z))
                self.mecanum_publisher.publish(twist_msg)
                # print("Twist", twist_msg)
            else:
                twist_msg.linear.x = 0.0
                twist_msg.linear.y = 0.0
                twist_msg.angular.z = 0.0
                self.mecanum_publisher.publish(twist_msg)
                
                self.STATE = States.X_CONTROL

        elif self.STATE == States.X_CONTROL:
            
            if abs(yaw_error) >= 0.3 or abs(x_error) >= 0.03:
                self.get_logger().info("YAW X Alignment")
                yaw_control = -(yaw_error * 0.001)

                x_control = x_error * 0.3
                twist_msg.linear.y = float(x_control)
                twist_msg.linear.y = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.linear.y))
                # print("X Control", x_control)

                twist_msg.angular.z = float(yaw_control)
                twist_msg.angular.z = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.angular.z))
                self.mecanum_publisher.publish(twist_msg)
                # print("Twist", twist_msg)
            else:
                twist_msg.linear.x = 0.0
                twist_msg.linear.y = 0.0
                twist_msg.angular.z = 0.0
                self.mecanum_publisher.publish(twist_msg)
                self.move_start_time = self.get_clock().now()
                self.get_logger().info("Starting MOVE_IN phase for 8 seconds")
                self.STATE = States.MOVE_IN

        elif self.STATE == States.MOVE_IN:
            current_time = self.get_clock().now()
            elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9

            if elapsed_time < self.move_duration:
                twist_msg.linear.x = self.wheel_speed
                self.mecanum_publisher.publish(twist_msg)
            else:
                twist_msg.linear.x = 0.0
                twist_msg.linear.y = 0.0
                twist_msg.angular.z = 0.0
                self.mecanum_publisher.publish(twist_msg)
                self.get_logger().info("Move_IN completed")
                self.STATE = States.MOVE_DOWN
        
        elif self.STATE == States.MOVE_DOWN:
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.angular.z = 0.0
            self.mecanum_publisher.publish(twist_msg)
            self.get_logger().info("Wait for forklift to move down")

        elif self.STATE == States.MOVE_OUT:
            current_time = self.get_clock().now()
            elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9

            if elapsed_time < self.move_duration:
                self.get_logger().info("Moving out")
                twist_msg.linear.x = -self.wheel_speed
                self.mecanum_publisher.publish(twist_msg)
            else:
                twist_msg.linear.x = 0.0
                twist_msg.linear.y = 0.0
                twist_msg.angular.z = 0.0
                self.mecanum_publisher.publish(twist_msg)
                self.get_logger().info("Move_OUT completed")
                self.STATE = States.DONE

        
        elif self.STATE == States.DONE:
            self.move_start_time = None
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.angular.z = 0.0
            self.mecanum_publisher.publish(twist_msg)
            # self.get_logger().info("Docking Z Alignment Done")
            # print("Yaw Error", yaw_error)
            # print("Z Error", z_error)
            # print("X Error", x_error)

        elif self.STATE == States.SEARCH_MARKER:
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.angular.z = 0.0
            self.mecanum_publisher.publish(twist_msg)
            self.get_logger().info("No Marker in view")



    

def main():
    rclpy.init()
    node = ShelfDockingNode()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        