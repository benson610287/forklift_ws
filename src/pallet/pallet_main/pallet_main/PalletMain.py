import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from geometry_msgs.msg import PoseStamped, Quaternion
from std_msgs.msg import Int64
from interface.srv import Maincontroller     # CHANGE
from moveit_driver.srv import Armcontrol
import math
import random
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time
class TurtlePControl(Node):
    def __init__(self):
        super().__init__('PalletMain')
        client_group1=ReentrantCallbackGroup()
        server_group=client_group1
        self.mainsrv = self.create_service(Maincontroller, 'Pallet', self.actived_callback,callback_group=server_group)        # CHANGE
        self.maniclient = self.create_client(Armcontrol, 'arm_cmd', callback_group = client_group1)
        
        # while not self.maniclient.wait_for_service(timeout_sec=1.0):
        #     self.get_logger().info('arm service not available, waiting again...')
        
        # # 移動平台命令
        self.mobile_position_publisher = self.create_publisher(PoseStamped, '/mobile_slam_topic', 10) #topic 名稱要改！！！
        self.ready_get_endpose_publisher = self.create_publisher(Int64,'/Pallet/endposeready',10)
        # # 手臂命令
        # self.arm_pose_publisher = self.create_publisher(Twist, '/arm_control', 10)   #topic和msg 名稱要改！！！
        self.real_startpose_subscriber = self.create_subscription(Twist, '/Pallet/realstartpose', self.startpose, 10)
        self.real_endpose_subscriber = self.create_subscription(Twist, '/Pallet/realendpose', self.endpose, 10)

        # # YOLO 命令
        self.yolo_cmd_publisher = self.create_publisher(Int64, '/Pallet/yolo_cmd', 10)  
        
        # self.timer = self.create_timer(0.1, self.state_machine_loop)  # 100ms 週期執行
        self.armstartpose=Twist()
        self.state = 'IDLE'  # 狀態機初始狀態
        self.currentstate = 'IDLE'
        self.startpose_received = False
        self.endpose_received = False
        self.homepose=[0.0,-550.0,500.0,180.0,0.0,0.0]
        self.photopose=[-618.53,-238.11,210.61,2.157*180/math.pi,2.289*180/math.pi,0.0]
        self.photopose=[-618.53,-205.11,564.61,180.0,0.0,0.0]
    # def actived_callback(self, request, response):
    #     if request.enable==True:
    #         self.mobile_move_to_unpack()
    #         yolo_cmd = Int64()
    #         yolo_cmd.data = 1
    #         self.yolo_cmd_publisher.publish(yolo_cmd)
    #         self.get_logger().info('Mobile platform moving to unpack position and YOLO command sent.')
            
    #         self.mobile_move_to_stack()



    #         response.done = 1                                                  # CHANGE
    #     else:
    #         response.done = 2
    #     self.get_logger().info('Incoming request\na: %d' % (response.done)) # CHANGE

    #     return response
    def actived_callback(self, request, response):
        if request.enable:
            self.get_logger().info('Service received, starting state machine...')
            self.state = 'MOVE_TO_HOME_POSE'

            # # 等到整個流程跑完再回傳
            # while self.state != 'DONE':
            #     # rclpy.spin_once(self, timeout_sec=0.1)
            #     time.sleep(0.01)
            while 1:
                # print (self.state)
                if self.state =='DONE':
                    self.get_logger().info('Task completed.')
                    break
                if self.state!=self.currentstate:
                    self.currentstate=self.state
                    self.state_machine_loop()
                else:
                    continue
            response.done = 1
        else: 
            response.done = 0
        self.currentstate = 'IDLE'
        self.state = 'IDLE'  # 重置狀態機
        return response
    def state_machine_loop(self):
        if self.state == 'IDLE':
            return

        elif self.state == 'MOVE_TO_HOME_POSE':
            self.get_logger().info('Moving to HOME_POSE...')
            self.move_to_home_pose()

        elif self.state == 'MOVE_TO_PHOTO_POSE':
            self.get_logger().info('Moving to PHOTO_POSE...')
            self.move_to_photo_pose()
            self.get_logger().info('Sending YOLO command...')
            
            self.state = 'WAIT_FOR_START_POSE'

        elif self.state == 'WAIT_FOR_START_POSE':
            self.yolo_cmd_publisher.publish(Int64(data=1))
            self.get_logger().info('Waiting for start pose...')

        elif self.state == 'MOVE_TO_STACK':
            self.get_logger().info('Moving to stack...')
            self.mobile_move_to_stack()
            self.state = 'WAIT_FOR_END_POSE'  # <<< 這會讓 callback 放行
        elif self.state == 'WAIT_FOR_END_POSE':
            self.get_logger().info('Waiting for end pose...')
        elif self.state == 'DONE':
            self.get_logger().info('Task completed.')

    def get_movepose_req(self,pose):
        inner_req = Armcontrol.Request()
        inner_req.pose.position.x = pose[0]/1000
        inner_req.pose.position.y = pose[1]/1000
        inner_req.pose.position.z = pose[2]/1000
        inner_req.pose.orientation=self.get_quaternion_from_euler(pose[3],pose[4],pose[5])
        self.get_logger().info("send pose.pose={}".format(inner_req.pose))
        input()
        return inner_req
    def move_to_home_pose(self):
        self.get_logger().info("starting home_pose...")
        inner_req=self.get_movepose_req(self.homepose)
        future = self.maniclient.call_async(inner_req)
        while not future.done():
            time.sleep(0.01)
            # print('a')
        try:
            inner_res = future.result()
            self.get_logger().info("home_pose_inner_res.done={}".format(inner_res.status))
            aa=inner_res.status
        except Exception as e:
            self.get_logger().error(f"shelf_pose Inner service failed: {e}")
            aa = -1
        if self.state == 'MOVE_TO_HOME_POSE':
            self.state = 'MOVE_TO_PHOTO_POSE'
    def move_to_photo_pose(self):
        self.get_logger().info("starting photo_pose...")
        inner_req=self.get_movepose_req(self.photopose)
        future = self.maniclient.call_async(inner_req)
        while not future.done():
            time.sleep(0.01)
        try:
            inner_res = future.result()
            self.get_logger().info("home_pose_inner_res.done={}".format(inner_res.status))
            aa=inner_res.status
        except Exception as e:
            self.get_logger().error(f"shelf_pose Inner service failed: {e}")
            aa = -1
        if self.state == 'MOVE_TO_PHOTO_POSE':
            self.state = 'DONE'
    def mobile_move_to_unpack(self):
        # 發佈移動平台命令
        mobile_cmd = PoseStamped()
        mobile_cmd.header.stamp = self.get_clock().now().to_msg()
        mobile_cmd.pose.position.x = 10
        mobile_cmd.pose.position.y = 10
        mobile_cmd.pose.position.z = 0
        mobile_cmd.pose.orientation = self.get_quaternion_from_euler(0, 0, 0)
        self.mobile_position_publisher.publish(mobile_cmd)
    def mobile_move_to_stack(self):
        # 發佈移動平台命令
        mobile_cmd = PoseStamped()
        mobile_cmd.header.stamp = self.get_clock().now().to_msg()
        mobile_cmd.pose.position.x = 0
        mobile_cmd.pose.position.y = 0
        mobile_cmd.pose.position.z = 0
        mobile_cmd.pose.orientation = self.get_quaternion_from_euler(0, 0, 0)
        self.mobile_position_publisher.publish(mobile_cmd)
    
    def get_quaternion_from_euler(self, roll, pitch, yaw):
        roll*=(math.pi/180.0)
        pitch*=(math.pi/180.0)
        yaw*=(math.pi/180.0)
        """Convert Euler angles to quaternion."""
        qx = math.sin(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) - math.cos(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        qy = math.cos(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2)
        qz = math.cos(roll / 2) * math.cos(pitch / 2) * math.sin(yaw / 2) - math.sin(roll / 2) * math.sin(pitch / 2) * math.cos(yaw / 2)
        qw = math.cos(roll / 2) * math.cos(pitch / 2) * math.cos(yaw / 2) + math.sin(roll / 2) * math.sin(pitch / 2) * math.sin(yaw / 2)
        return Quaternion(x=qx, y=qy, z=qz, w=qw)

    def startpose(self, msg):
        if self.startpose_received:
            self.get_logger().warn('Start pose already received, ignoring new message.')
            return
        self.startpose_received = True
        self.get_logger().info('Received real pose, moving to pick...')
        startpose=[msg.linear.x,msg.linear.y,msg.linear.z,msg.angular.x,msg.angular.y,msg.angular.z]
        inner_req=self.get_movepose_req(startpose+[0.0,0.0,50.0,0.0,0.0,0.0])
        future = self.maniclient.call_async(inner_req)
        while not future.done():
            time.sleep(0.01)
        try:
            inner_res = future.result()
            self.get_logger().info("start_pose_inner_res.done={}".format(inner_res.status))
            aa=inner_res.status
        except Exception as e:
            self.get_logger().error(f"start_pose Inner service failed: {e}")
            aa = -1
        
        inner_req=self.get_movepose_req(startpose)
        future = self.maniclient.call_async(inner_req)
        while not future.done():
            time.sleep(0.01)
        try:
            inner_res = future.result()
            self.get_logger().info("start_pose_inner_res.done={}".format(inner_res.status))
            aa=inner_res.status
        except Exception as e:
            self.get_logger().error(f"start_pose Inner service failed: {e}")
            aa = -1
        if self.state == 'WAIT_FOR_START_POSE':
            self.state = 'DONE'

    def endpose(self, msg):
        if self.endpose_received:
            self.get_logger().warn('End pose already received, ignoring new message.')
            return
        self.endpose_received = True
        self.get_logger().info('Received real end pose, moving to stack...')
        self.armendpose = msg
        # 發佈手臂命令
        # self.arm_pose_publisher.publish(self.armendpose)
        inner_req = Armcontrol.Request()
        inner_req.pose.position.x = msg.linear.x
        inner_req.pose.position.y = msg.linear.y
        inner_req.pose.position.z = msg.linear.z
        inner_req.pose.theta=self.get_quaternion_from_euler(msg.angular.x,msg.angular.y,msg.angular.z)
        future = self.maniclient.call_async(inner_req)
        while not future.done():
            time.sleep(0.01)
        try:
            inner_res = future.result()
            print("shelf_pose_inner_res.done=",inner_res.status)
            aa=inner_res.status
        except Exception as e:
            self.get_logger().error(f"shelf_pose Inner service failed: {e}")
            aa = -1
        if self.state == 'WAIT_FOR_END_POSE':
            self.state = 'DONE'

    def control_loop(self):
        pass


def main(args=None):
    rclpy.init(args=args)
    node = TurtlePControl()
    executor=MultiThreadedExecutor()
    executor.add_node(node)
    executor.spin()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()