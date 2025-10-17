import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseArray, Twist
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int64, Float32MultiArray, Int32
from interface.srv import Maincontroller, Slidecmd 
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


class LinearControlNode(Node):
    def __init__(self,share_data):
        super().__init__('linear_control_node')
        self.share_data=share_data
        self.last_pos=0
        self.timer_group = MutuallyExclusiveCallbackGroup()
        self.pose_group = MutuallyExclusiveCallbackGroup()

        self.linear_motor_cli = self.create_client(Slidecmd, 'linear/move_cmd')
        while not self.linear_motor_cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Linear motor service not available, waiting again...')
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.call_linear_motor,callback_group=self.timer_group)
        self.first_flag = True
        self.get_logger().info(f"opening ")

    def call_linear_motor(self):
        if self.share_data["linear_req"].pos != self.last_pos and not self.first_flag:
            req = self.share_data["linear_req"]
            # req.pos = position
            self.future = self.linear_motor_cli.call_async(req)
            # rclpy.spin_until_future_complete(self, self.future)
            # self.share_data["linear_res"] = self.future.result()
            self.future.add_done_callback(self.first_move_callback)

            self.last_pos=self.share_data["linear_req"].pos
            self.get_logger().info(f"Linear req:{self.share_data['linear_req'].pos} (res: {self.share_data['linear_res'].done})")
        elif self.first_flag:
            req = Slidecmd.Request()
            req.pos = 0
            self.future = self.linear_motor_cli.call_async(req)
            # rclpy.spin_until_future_complete(self, self.future)
            # self.future.add_done_callback(self.first_move_callback)
            self.last_pos=req.pos
            self.first_flag= False
            self.share_data["linear_res"].done = False
            self.get_logger().info(f"first move Linear req:{self.share_data['linear_req'].pos}")


    def first_move_callback(self, future):
        try:
            response = future.result()
            # if  self.first_flag:
            #     response.done=False
            #     self.get_logger().info(f"First move completed")
            # self.last_pos = 0
            self.share_data["linear_res"].done=response.done 
            self.get_logger().info(f"move completed: {response.done}")
        except Exception as e:
            self.get_logger().error(f'move service call failed: {e}')


class ShelfDockingNode(Node):
    def __init__(self,share_data):
        super().__init__('shelf_docking_node')
        self.share_data=share_data

        self.timer_group = MutuallyExclusiveCallbackGroup()
        self.pose_group = MutuallyExclusiveCallbackGroup()


        self.service = self.create_service(Maincontroller, '/shelf_docking', self.service_callback)

        self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 100,callback_group=self.pose_group)
        
        # self.linear_motor_publisher = self.create_publisher(Int64, 'linear/move_cmd', 10)
        self.mecanum_publisher = self.create_publisher(Twist, '/cmd_vel', 1)
        self.shelf_state_subscriber = self.create_subscription(ShelfState, '/shelf/state', self.shelf_callback, 10,callback_group=self.pose_group)
        # self.linear_state_subscriber = self.create_subscription(Int64, 'linear/move_state', self.linear_callback, 10,callback_group=self.pose_group)


        # self.aaa_subscriber = self.create_subscription(Int64, 'start', self.pose_process, 10,callback_group=self.control_group)

        self.linear_motor_timer = self.create_timer(1.0, self.publish_linear_motor,callback_group=self.timer_group)

        # SLAM
        self.slam_pose_publisher = self.create_publisher(Float32MultiArray, '/timda_nav_pose', 10, callback_group=self.pose_group)
        self.slam_success_subscriber = self.create_subscription(Int32, '/timda_nav_success', self.slam_success_callback, 10, callback_group=self.pose_group)

        self.linear_motor_timer.cancel()

        # state and parameter initialization
        self.active = False
        self.max_coontrol_vel = 0.2
        self.z_target = 1.60 #1.55 meters away from marker
        self.x_left_target = 0.07
        self.x_right_target = -0.60
        self.move_in = None
        self.move_out = None
        # self.STATE = States.YAW_CONTROL
        self.STATE = States.MOVE_CAR

        self.move_start_time = None
        dis_const = 1.1
        # dis_const = 0.5
        self.wheel_speed = 0.1
        self.move_duration = dis_const/self.wheel_speed

        # shelf state 
        self.lock_shelf_state = None
        self.mock_shelf_state = [1,1,1,1,1,1,1,1]

        # shelf pose
        self.pose = None

        # SLAM pose init
        self.slam_shelf_left = Float32MultiArray()
        self.slam_shelf_right = Float32MultiArray()
        self.slam_shelf_left.data = [4.1, -1.4, 90.0]
        self.slam_shelf_right.data = [2.6, -1.4, 90.0]
        self.slam_success = 888

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

    def slam_success_callback(self, msg):
        self.slam_success = msg.data
        print("Slam success:", self.slam_success)
        

    def pose_callback(self, msg):
        self.pose = msg.poses[1]
        if any([self.pose.position.x, self.pose.position.y, self.pose.position.z]):
            pass
        else:
            self.pose = msg.poses[3]
            if any([self.pose.position.x, self.pose.position.y, self.pose.position.z]):
                pass
        # self.get_logger().info(f"Pose :{self.pose.position.x, self.pose.position.y, self.pose.position.z}")

    # def linear_callback(self, msg):
    #     print("Linear msg", msg)
    #     self.linear_state = msg.data

    def shelf_callback(self, msg):
        print("shelf state data:", msg.shelf_state)  #shelf state data: [False, False, False, False, True, True, False, False]
        print("TYPE:", type(msg.shelf_state))        #TYPE: <class 'list'>
        self.shelf_state = msg.shelf_state

    def publish_linear_motor(self):
        # self.linear_event.wait()
        self.get_logger().info(f"(State: {self.STATE.name})")
        # linear_msg = Int64()

        if self.lock_shelf_state is None:
            move_in_height = 98
            move_out_height = 90
        else:
            move_in_height = self.move_in_height
            move_out_height = self.move_out_height


        if self.STATE == States.YAW_CONTROL or self.STATE == States.X_CONTROL:
            # linear_msg.data = move_in_height
            # self.linear_motor_publisher.publish(linear_msg)
            self.share_data["linear_req"].pos=move_in_height
            self.get_logger().info(f"Linear Motor:{self.share_data['linear_req'].pos} (State: {self.STATE.name})")
            # self.mobile_event.set()
        
        
        elif self.STATE == States.MOVE_CAR:
            # linear_msg.data = 30
            # self.linear_motor_publisher.publish(linear_msg)
            self.share_data["linear_req"].pos=30
            self.get_logger().info(f"Linear Motor:{self.share_data['linear_req'].pos} (State: {self.STATE.name})")
            # time.sleep(0.5)
            # while self.linear_state==0:
            #     time.sleep(0.01)
            #     pass
            # self.mobile_event.set()
        
        elif self.STATE == States.MOVE_IN:
            # linear_msg.data = move_in_height
            # self.linear_motor_publisher.publish(linear_msg)
            self.share_data["linear_req"].pos=move_in_height
            self.get_logger().info(f"Linear Motor:{self.share_data['linear_req'].pos} (State: {self.STATE.name})")
            # time.sleep(0.5)
            # while self.linear_state==0:
            #     time.sleep(0.01)
            #     pass
            # self.move_start_time = self.get_clock().now()
            # self.STATE = States.MOVE_OUT 
            # time.sleep(2.0)
            # self.mobile_event.set()

        elif self.STATE == States.MOVE_DOWN:
            # linear_msg.data = move_out_height
            # self.linear_motor_publisher.publish(linear_msg)
            self.share_data["linear_req"].pos=move_out_height
            self.get_logger().info(f"Linear Motor:{self.share_data['linear_req'].pos} (State: {self.STATE.name})")
            # time.sleep(0.5)
            # while self.linear_state==0:
            #     time.sleep(0.01)
            #     pass
            # self.move_start_time = self.get_clock().now()
            # self.STATE = States.MOVE_OUT 
            # time.sleep(2.0)
            # self.mobile_event.set()

        elif self.STATE == States.MOVE_OUT:
            # linear_msg.data = move_out_height
            # self.linear_motor_publisher.publish(linear_msg)
            self.share_data["linear_req"].pos=move_out_height
            self.get_logger().info(f"Linear Motor:{self.share_data['linear_req'].pos} (State: {self.STATE.name})")

        elif self.STATE == States.DONE:
            # time.sleep(3.0)
            # linear_msg.data = 0
            # self.linear_motor_publisher.publish(linear_msg)
            self.share_data["linear_req"].pos = 0
            self.get_logger().info(f"Linear Motor:{self.share_data['linear_req'].pos} (State: {self.STATE.name})")
            # self.get_logger().info(f"Linear motor stopped: {linear_msg.data}")
            # time.sleep(0.5)
            # while self.linear_state==0:
            #     time.sleep(0.01)
            #     pass
            self.linear_motor_timer.cancel()
            # self.mobile_event.set()
        else:
            # linear_msg.data = 0
            # self.linear_motor_publisher.publish(linear_msg)
            pass

    # def pose_process(self,msg):
    #     print("process=", msg)
    def service_callback(self, request, response):
        self.slam_success = 888
        print("REQUEST: ", request.enable)
        if not request.enable and self.active:
            self.get_logger().info("Deactivate shelf docking, but just logging, no actually deactivation ")
            self.active = False
            pass
        
        elif (request.enable and self.active) or (not request.enable and not self.active):
            response.done = 2
            self.get_logger().info(f"Shelf docking already in requested state")
        
        else: # request.enable and not self.active
            self.active = True
            self.linear_motor_timer.reset()
            last_z_error = None
            last_x_error = None

            control_start_time = self.get_clock().now()

            while self.STATE!=States.DONE:
                # quat = [self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z, self.pose.orientation.w]
                # r = R.from_quat(quat)
                # euler_angles = r.as_euler('xyz', degrees=True)
                # yaw_error = euler_angles[1]

                # z_value = self.pose.position.z
                # z_error = z_value - self.z_target

                # x_value = self.pose.position.x
                # x_error = self.x_right_target - x_value

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
                    
                    # self.mobile_event.wait()
                    # self.mobile_event.clear()
                    while self.share_data["linear_res"].done != True:
                        pass
                    
                    print("Move car using slam")
                    if self.slam_success == 888:
                        self.slam_pose_publisher.publish(self.slam_shelf_right)
                        self.slam_success=None
                    else:
                        if self.slam_success == 1:
                            self.get_logger().info("SLAM navigation success!!")
                            self.share_data["linear_res"].done = False
                            self.STATE = States.YAW_CONTROL
                            
                        elif self.slam_success == 2:
                            self.get_logger().info("SLAM navigation failed")

                elif self.STATE == States.YAW_CONTROL:
                    quat = [self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z, self.pose.orientation.w]
                    r = R.from_quat(quat)
                    euler_angles = r.as_euler('xyz', degrees=True)
                    yaw_error = euler_angles[1]

                    z_value = self.pose.position.z
                    z_error = z_value - self.z_target

                    x_value = self.pose.position.x
                    x_error = self.x_right_target - x_value

                    if abs(yaw_error) >= 0.3 or abs(z_error) >= 0.03:
                        self.get_logger().info("YAW Z Alignment")

                        if last_z_error is not None:
                            z_error_dt = (z_error - last_z_error) / 0.1
                        else:
                            z_error_dt = 0

                        yaw_control = -(yaw_error * 0.002)

                        z_control = z_error * 0.2 + z_error_dt * 0.3
                        twist_msg.linear.x = float(z_control)
                        twist_msg.linear.x = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.linear.x))

                        twist_msg.angular.z = float(yaw_control)
                        twist_msg.angular.z = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.angular.z))
                        self.mecanum_publisher.publish(twist_msg)
                        time.sleep(0.1)
                    else:
                        control_end_time = self.get_clock().now()
                        control_time = (control_end_time - control_start_time).nanoseconds / 1e9
                        twist_msg.linear.x = 0.0
                        twist_msg.linear.y = 0.0
                        twist_msg.angular.z = 0.0
                        self.mecanum_publisher.publish(twist_msg)
                        print(f"Yaw Control Time Taken: {control_time} seconds")
                        print("+++++++++++++++++++++++++++++++++++++++++++")
                        print("===========================================")
                        self.STATE = States.X_CONTROL       
                        

                elif self.STATE == States.X_CONTROL:
                    quat = [self.pose.orientation.x, self.pose.orientation.y, self.pose.orientation.z, self.pose.orientation.w]
                    r = R.from_quat(quat)
                    euler_angles = r.as_euler('xyz', degrees=True)
                    yaw_error = euler_angles[1]

                    z_value = self.pose.position.z
                    z_error = z_value - self.z_target

                    x_value = self.pose.position.x
                    x_error = self.x_right_target - x_value

                    if abs(yaw_error) >= 0.3 or abs(x_error) >= 0.03:
                        self.get_logger().info("YAW X Alignment")

                        if last_x_error is not None:
                            x_error_dt = (x_error - last_x_error) / 1.0
                        else:
                            x_error_dt = 0
                        
                        yaw_control = -(yaw_error * 0.002)

                        x_control = x_error * 0.2 + x_error_dt * 0.3
                        twist_msg.linear.y = float(x_control)
                        twist_msg.linear.y = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.linear.y))
                        # print("X Control", x_control)

                        twist_msg.angular.z = float(yaw_control)
                        twist_msg.angular.z = max(-self.max_coontrol_vel, min(self.max_coontrol_vel, twist_msg.angular.z))
                        self.mecanum_publisher.publish(twist_msg)
                        time.sleep(1.0)
                        # print("Twist", twist_msg)
                    else:
                        twist_msg.linear.x = 0.0
                        twist_msg.linear.y = 0.0
                        twist_msg.angular.z = 0.0
                        self.mecanum_publisher.publish(twist_msg)
                        self.STATE = States.MOVE_IN
                        
                            

                elif self.STATE == States.MOVE_IN:
                    twist_msg.linear.x = 0.0
                    twist_msg.linear.y = 0.0
                    twist_msg.angular.z = 0.0
                    self.mecanum_publisher.publish(twist_msg)
                    self.get_logger().info("Wait for forklift to reach")
                    # self.mobile_event.wait()
                    # self.mobile_event.clear()
                    while self.share_data["linear_res"].done != True:
                        pass
                    self.share_data["linear_res"].done = False

                    self.move_start_time = self.get_clock().now()
                    self.get_logger().info(f"Starting MOVE_IN phase for {self.move_duration} seconds")
                    current_time = self.get_clock().now()
                    elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9
                    twist_msg.linear.x = self.wheel_speed
                    self.mecanum_publisher.publish(twist_msg)
                    
                    while elapsed_time < self.move_duration:
                        current_time = self.get_clock().now()
                        elapsed_time = (current_time - self.move_start_time).nanoseconds / 1e9
                    twist_msg.linear.x = 0.0
                    twist_msg.linear.y = 0.0
                    twist_msg.angular.z = 0.0
                    self.mecanum_publisher.publish(twist_msg)
                    self.get_logger().info("Move_IN completed")
                    self.STATE = States.MOVE_DOWN
                    # time.sleep(3.0)


                elif self.STATE == States.MOVE_DOWN:
                    
                    twist_msg.linear.x = 0.0
                    twist_msg.linear.y = 0.0
                    twist_msg.angular.z = 0.0
                    self.mecanum_publisher.publish(twist_msg)
                    self.get_logger().info("Wait for forklift to move down")
                    # self.mobile_event.wait()
                    # self.mobile_event.clear()
                    while self.share_data["linear_res"].done != True:
                        pass
                    self.share_data["linear_res"].done = False
                    # self.linear_motor_timer.cancel()
                    # linear_msg = Int64()
                    # linear_msg.data = 20
                    # self.linear_motor_publisher.publish(linear_msg)
                    time.sleep(4.0)
                    
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

                    # Stop linear motor in move out state
                    # linear_msg = Int64()
                    # linear_msg.data = 0
                    # self.linear_motor_publisher.publish(linear_msg)
 
                    # self.get_logger().info(f"Linear motor stopped: {linear_msg.data}")
                    # self.linear_motor_timer.reset()
                    self.STATE = States.DONE
                    

                
                elif self.STATE == States.DONE:
                    self.move_start_time = None
                    twist_msg.linear.x = 0.0
                    twist_msg.linear.y = 0.0
                    twist_msg.angular.z = 0.0
                    self.mecanum_publisher.publish(twist_msg)
                    while self.share_data["linear_res"].done != True:
                        pass
                    self.get_logger().info("Done")
                    # self.get_logger().info("Docking Z Alignment Done")
                    # print("Yaw Error", yaw_error)
                    # print("Z Error", z_error)
                    # print("X Error", x_error)
                    
                #     self.linear_motor_timer.reset()
                    # self.linear_event.set()

                elif self.STATE == States.SEARCH_MARKER:
                    twist_msg.linear.x = 0.0
                    twist_msg.linear.y = 0.0
                    twist_msg.angular.z = 0.0
                    self.mecanum_publisher.publish(twist_msg)
                    self.get_logger().info("No Marker in view")

            self.get_logger().info("Wait for linear complete")
            # self.mobile_event.wait()
            # self.mobile_event.clear()
            while self.share_data["linear_res"].done != True:
                pass
            self.share_data["linear_res"].done = False
            self.get_logger().info("DONE sequence completed")
            self.linear_motor_timer.cancel()
            time.sleep(1.5)
            self.STATE = States.MOVE_CAR
            self.linear_flag=False
            self.active = False
            response.done = 0
            self.get_logger().info(f"Response is {response.done}")
            return response
        




def main():
    rclpy.init()
    share_data={"linear_req": Slidecmd.Request(), "linear_res": Slidecmd.Response()}
    share_data["linear_res"].done = False
    ShelfDocking_node = ShelfDockingNode(share_data)
    linear_control_node = LinearControlNode(share_data)
    executor = MultiThreadedExecutor()
    # executor = MultiThreadedExecutor(num_threads=7)
    executor.add_node(ShelfDocking_node)
    executor.add_node(linear_control_node)
    executor.spin()
    ShelfDocking_node.destroy_node()
    linear_control_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
        