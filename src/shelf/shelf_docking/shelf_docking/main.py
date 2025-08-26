import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseArray, Twist
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int64
from interface.srv import Maincontroller
from interface.msg import ShelfState
from cv_bridge import CvBridge
import os
import configparser
from interface.srv import Maincontroller
import numpy as np
from scipy.spatial.transform import Rotation as R
import time


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

        self.active = False

        self.pid_x = PID(1.0, 0.0, 0.1)
        self.pid_z = PID(1.0, 0.0, 0.1)
        self.pid_yaw = PID(0.0002, 0.0, 0.1)

        self.max_angular_vel = 0.2
        self.last_yaw_error = 0.0

        self.STATE = 0

        # self.last_time = None
        # self.target_yaw = 0.0


    # def service_callback(self, request, response):
    #     if request.enable and not self.active:
    #         self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 10)
    #         self.linear_motor_publisher = self.create_publisher(Int64, '/topic', 10)
    #         self.mecanum_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
    #         self.active = True


    #     elif not request.enable and self.active:
    #         self.destroy_subscription(self.shelf_pose_subscriber)
    #         self.destroy_publisher(self.linear_motor_publisher)
    #         self.destroy_publisher(self.mecanum_publisher)
    #         self.active = False
        

    def pose_callback(self, msg):
        
        # current_time = self.get_clock().now().nanoseconds / 1e9 #use nanoseconds then convert to seconds for percision
        # if self.last_time is None:
        #     self.last_time = current_time
        #     return # Skip first iteration to astablish timing
        
        # dt = current_time - self.last_time
        # self.last_time = current_time

        # check marker 0 and 3 because there is either 0 or 3 visible to camera at a time


        pose = msg.poses[0]
        if any([pose.position.x, pose.position.y, pose.position.z]):
            pass
        else:
            pose = msg.poses[3]
        
        quat = [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]
        r = R.from_quat(quat)
        euler_angles = r.as_euler('xyz', degrees=True)
        yaw_error = euler_angles[1]
        # derivative = yaw_error - self.last_yaw_error
        # self.last_yaw_error = yaw_error

        if self.STATE == 0:
            if abs(yaw_error) >= 0.3:
                self.get_logger().info("Docking Alignment")
                yaw_control = -(yaw_error * 0.001)
                print("+++++++++++++++++++++")
                print("Yaw Error", yaw_error)
                print("Yaw Control", yaw_control)

                twist_msg = Twist()
                twist_msg.angular.z = float(yaw_control)
                twist_msg.angular.z = max(-self.max_angular_vel, min(self.max_angular_vel, twist_msg.angular.z))
                self.mecanum_publisher.publish(twist_msg)
                # print("Twist", twist_msg)
            else:
                print("+++++++++++++++++++++")
                print("Yaw Error", yaw_error)
                twist_msg = Twist()
                self.mecanum_publisher.publish(twist_msg)
                
                self.STATE = 1
        elif self.STATE == 1:
            twist_msg = Twist()
            self.mecanum_publisher.publish(twist_msg)
            print("Twist Msg", twist_msg)
            self.get_logger().info("Docking Alignment Done")




    

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
        