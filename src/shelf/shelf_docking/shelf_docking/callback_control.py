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


from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
import threading as Thread

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
    FINISH = 11

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


        self.timer_group = MutuallyExclusiveCallbackGroup()
        self.pose_group = MutuallyExclusiveCallbackGroup()
        self.control_group = MutuallyExclusiveCallbackGroup()
        self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 10)
        # self.service = self.create_service(Maincontroller, 'shelf_docking', self.service_callback)
        self.linear_motor_publisher = self.create_publisher(Int64, 'linear/move_cmd', 10)
        self.mecanum_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.shelf_state_subscriber = self.create_subscription(ShelfState, '/shelf/state', self.shelf_callback, 10)
        self.linear_state_subscriber = self.create_subscription(Int64, 'linear/move_state', self.linear_callback, 10)

        # self.linear_motor_timer = self.create_timer(1.0, self.publish_linear_motor)
        # self.linear_motor_timer.cancel()


        self.active = False
        self.max_coontrol_vel = 0.2
        self.z_target = 1.45 #1.45 meters away from marker
        self.x_left_target = 0.07
        self.x_right_target = -0.64
        self.move_in = None
        self.move_out = None
        self.STATE = States.YAW_CONTROL

        self.move_start_time = None
        dis_const = 20
        self.wheel_speed = 0.1
        self.move_duration = dis_const * self.wheel_speed

        self.lock_shelf_state = None

        self.pose = None
    
        # self.linear_event=Thread.Event()
        # self.mobile_event=Thread.Event()
        # self.linear_event.clear()
        # self.mobile_event.clear()

    # def service_callback(self, request, response):
    #     if request.enable and not self.active:
    #         self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 10)
    #         self.linear_motor_publisher = self.create_publisher(Int64, 'linear/move_cmd', 10)
    #         self.mecanum_publisher = self.create_publisher(Twist, '/cmd_vel', 10)
    #         self.shelf_state_subscriber = self.create_subscription(ShelfState, '/shelf/state', self.shelf_callback, 10)
    #         self.active = True

    #     elif not request.enable and self.active:
    #         self.destroy_subscription(self.shelf_pose_subscriber)
    #         self.destroy_publisher(self.linear_motor_publisher)
    #         self.destroy_publisher(self.mecanum_publisher)
    #         self.active = False

    def linear_callback(self, msg):
        print("Linear msg", msg)
        self.linear_state = msg.data

    def shelf_callback(self, msg):
        print("shelf state data:", msg.shelf_state)  #shelf state data: [False, False, False, False, True, True, False, False]
        print("TYPE:", type(msg.shelf_state))        #TYPE: <class 'list'>
        self.shelf_state = msg.shelf_state

    def publish_linear_motor(self):
        # self.linear_event.wait()
        self.get_logger().info(f"(State: {self.STATE.name})")
        linear_msg = Int64()

        if self.lock_shelf_state is None:
            move_in_height = 30
            move_out_height = 20
        else:
            move_in_height = self.move_in_height
            move_out_height = self.move_out_height


        if self.STATE == States.YAW_CONTROL or self.STATE == States.X_CONTROL or self.STATE == States.MOVE_IN or self.STATE == States.MOVE_CAR:
            linear_msg.data = move_in_height
            self.linear_motor_publisher.publish(linear_msg)
            self.get_logger().info(f"Linear Motor:{linear_msg.data} (State: {self.STATE.name})")
            # self.mobile_event.set()

        elif self.STATE == States.MOVE_DOWN:
            linear_msg.data = move_out_height
            self.linear_motor_publisher.publish(linear_msg)
            # time.sleep(0.5)
            while self.linear_state==0:
                pass
            # self.move_start_time = self.get_clock().now()
            # self.STATE = States.MOVE_OUT 
            # self.mobile_event.set()

        elif self.STATE == States.MOVE_OUT:
            linear_msg.data = move_out_height
            self.linear_motor_publisher.publish(linear_msg)

        elif self.STATE == States.DONE:
            time.sleep(3.0)
            linear_msg.data = 0
            self.linear_motor_publisher.publish(linear_msg)
            self.get_logger().info(f"Linear motor stopped: {linear_msg.data}")
            # time.sleep(0.5)
            while self.linear_state==0:
                pass
            # self.linear_motor_timer.cancel()
            # self.mobile_event.set()
        else:
            # linear_msg.data = 0
            # self.linear_motor_publisher.publish(linear_msg)
            pass

    # WHY USE CALLBACK FUNCTION TO DO CONTROL ?
    # BECAUSE IT MATCH THE FRAME WITHOUT TIMING (THE CONTROL SIGNAL COMES FROM THE EXACT MARKER)
    def pose_callback(self,msg):

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
        if self.STATE == States.LOCK_SHELF_STATE:
            self.lock_shelf_state = self.shelf_state
            for i, state in enumerate(self.lock_shelf_state):
                if i < 4 and state == True:
                    print("Move car to left shelf")
                    if i < 3 and state == True:
                        self.move_in_height = 98
                        self.move_out_height = 90
                        print("Move liear to upper shelf")
                    else:
                        self.move_in_height = 30
                        self.move_out_height = 20
                        print("Move liear to lower shelf")
                    break
                elif i >= 4 and state == True:
                    print("Move car to right shelf")
                    if i < 6 and state == True:
                        self.move_in_height = 98
                        self.move_out_height = 90
                        print("Move liear to upper shelf")
                    else:
                        self.move_in_height = 30
                        self.move_out_height = 20
                        print("Move liear to lower shelf")
                else:
                    print("All shelfs are occupied")
            self.STATE = States.MOVE_CAR

        elif self.STATE == States.MOVE_CAR:
            print("Move car using slam")
            
            self.STATE = States.YAW_CONTROL

        elif self.STATE == States.YAW_CONTROL:
            if abs(yaw_error) >= 0.3 or abs(z_error) >= 0.03:
                
                self.get_logger().info("YAW Z Alignment")
                yaw_control = -(yaw_error * 0.001)

                z_control = z_error * 0.3
                twist_msg.linear.x = float(z_control)
                twist_msg.linear.x = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.linear.x))

                twist_msg.angular.z = float(yaw_control)
                twist_msg.angular.z = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.angular.z))
                self.mecanum_publisher.publish(twist_msg)
            else:
                time.sleep(0.3)
                twist_msg.linear.x = 0.0
                twist_msg.linear.y = 0.0
                twist_msg.angular.z = 0.0
                self.mecanum_publisher.publish(twist_msg)
                print("+++++++++++++++++++++++++++++++++++++++++++")
                print("===========================================")
                time.sleep(3.0)
                self.STATE = States.X_CONTROL
                
                

        elif self.STATE == States.X_CONTROL:
            if abs(yaw_error) >= 0.3 or abs(x_error) >= 0.03:
                self.get_logger().info("YAW X Alignment")
                yaw_control = -(yaw_error * 0.001)

                x_control = x_error * 0.3
                twist_msg.linear.y = float(x_control)
                twist_msg.linear.y = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.linear.y))

                twist_msg.angular.z = float(yaw_control)
                twist_msg.angular.z = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.angular.z))
                self.mecanum_publisher.publish(twist_msg)
            else:
                time.sleep(0.3)
                twist_msg.linear.x = 0.0
                twist_msg.linear.y = 0.0
                twist_msg.angular.z = 0.0
                self.mecanum_publisher.publish(twist_msg)
                print("+++++++++++++++++++++++++++++++++++++++++++")
                print("===========================================")
                time.sleep(3.0)
                self.STATE = States.MOVE_IN                    

        elif self.STATE == States.MOVE_IN:
            self.move_start_time = self.get_clock().now()
            self.get_logger().info(f"Starting MOVE_IN phase for {self.move_duration} seconds")
            current_time = self.get_clock().now()
            elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9
            twist_msg.linear.x = self.wheel_speed
            self.mecanum_publisher.publish(twist_msg)
            
            while elapsed_time < self.move_duration:
                current_time = self.get_clock().now()
                elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9
            time.sleep(0.3)
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.angular.z = 0.0
            self.mecanum_publisher.publish(twist_msg)
            self.get_logger().info("Move_IN completed")
            print("<><><><><><><><><><><><><><><><><><><><><><><>")
            time.sleep(3.0)
            self.STATE = States.MOVE_DOWN

        elif self.STATE == States.MOVE_DOWN:
            
            twist_msg.linear.x = 0.0
            twist_msg.linear.y = 0.0
            twist_msg.angular.z = 0.0
            self.mecanum_publisher.publish(twist_msg)
            self.get_logger().info("Wait for forklift to move down")
            # self.mobile_event.wait()
            # self.mobile_event.clear()
            # self.linear_motor_timer.cancel()

            # linear_msg = Int64()
            # linear_msg.data = 20
            # self.linear_motor_publisher.publish(linear_msg)
            # time.sleep(4.0)
            
            self.get_logger().info("MOVE_DOWN completed")
            self.STATE = States.MOVE_OUT 


        elif self.STATE == States.MOVE_OUT:
            self.get_logger().info("MOVE_OUT start")
            
            self.move_start_time = self.get_clock().now()
            current_time = self.get_clock().now()
            elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9
            self.get_logger().info("Moving out")
            twist_msg.linear.x = -self.wheel_speed
            self.mecanum_publisher.publish(twist_msg)

            while elapsed_time < self.move_duration:
                current_time = self.get_clock().now()
                elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9
            time.sleep(0.3)
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

            
            # self.linear_motor_timer.reset()
            # self.linear_event.set()

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
        