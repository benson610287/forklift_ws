import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from geometry_msgs.msg import Twist

class YoloCmdNode(Node):
    def __init__(self):
        super().__init__('single_arm_start_end')
        self.yolo_cmd_pub = self.create_publisher(Int64, '/Pallet/yolo_cmd', 10)
        self.endposeready_sub = self.create_subscription(Int64,'Pallet/single/endposeready',self.sendendpose,10)
        self.virtual_startpose_sub = self.create_subscription(Twist, '/Pallet/single/virtualstartpose', self.startpose, 10)
        self.real_startpose_pub = self.create_publisher(Twist, '/Pallet/single/realstartpose', 10)
        self.virtual_endpose_sub = self.create_subscription(Twist, '/Pallet/Single/virtualendpose', self.endpose, 10)
        self.real_endpose_pub = self.create_publisher(Twist, '/Pallet/single/realendpose', 10)
        self.stack_full_pub = self.create_publisher(Int64, '/Pallet/single/multistackfull', 10)
        self.create_timer(0.1, self.loop)
        self.sensor_flag=True
        self.startflag=False
        self.endflag=False

        self.base_pose = [409.0-800.0,-856.0,-341.0,180.0,0.0,0.0]  # 預設基座位姿
        self.eyetohand=[-100.0,20.0,0.0,0.0,0.0,0.0]
    def loop(self):
        if self.startflag and self.endflag:
            self.get_logger().info(f"Publishing real start pose: {self.real_startpose}")
            self.real_startpose_pub.publish(self.real_startpose)
            self.startflag=False
        else:
            pass
    def startpose(self, msg):
        self.startflag=True
        self.get_logger().info(f"Received virtual start pose: {msg}")
        # self.sensor_flag=msg

        self.real_startpose = Twist()
        self.real_startpose.linear.x = -msg.linear.y+self.eyetohand[0]
        self.real_startpose.linear.y = -msg.linear.x+self.eyetohand[1]
        if 70.0<msg.linear.z<90.0:
            self.real_startpose.linear.z = -65.0 +self.eyetohand[2]
        else:
            self.real_startpose.linear.z = -265.0 +self.eyetohand[2]
        self.real_startpose.angular.x = 0.0
        self.real_startpose.angular.y = 0.0
        self.real_startpose.angular.z = 0.0
        # real_startpose.linear.x = self.base_pose[0]
        # real_startpose.linear.y = self.base_pose[1]
        # real_startpose.linear.z = self.base_pose[2] 
        # real_startpose.angular.x =  self.base_pose[3]
        # real_startpose.angular.y = self.base_pose[4]
        # real_startpose.angular.z = self.base_pose[5]
        
    def endpose(self, msg):
        self.get_logger().info(f"Received virtual end pose: {msg}")
        
        if msg.linear.x==-1.0 and msg.linear.y==-1.0 and msg.linear.z==-1.0 and msg.angular.z==-1.0:
            self.endflag=False
            stackfull=Int64()
            stackfull.data=int(1)
            self.stack_full_pub.publish(stackfull)
            self.get_logger().info(f"Publishing stackfull state: {stackfull}")
        else:
            self.endflag=True
            self.real_endpose = Twist()
            self.real_endpose.linear.x = msg.linear.x + self.base_pose[0]
            self.real_endpose.linear.y = msg.linear.y + self.base_pose[1]
            self.real_endpose.linear.z = msg.linear.z + self.base_pose[2]
            self.real_endpose.angular.x = msg.angular.x + self.base_pose[3]
            self.real_endpose.angular.y = msg.angular.y + self.base_pose[4]
            self.real_endpose.angular.z = msg.angular.z + self.base_pose[5]
            # self.real_endpose.linear.x =  self.base_pose[0]
            # self.real_endpose.linear.y = self.base_pose[1]
            # self.real_endpose.linear.z = self.base_pose[2]
            # self.real_endpose.angular.x =  self.base_pose[3]
            # self.real_endpose.angular.y = self.base_pose[4]
            # self.real_endpose.angular.z = self.base_pose[5]
        
    def sendendpose(self,msg):
        if self.endflag==True:
            
            self.get_logger().info(f"Publishing real end pose: {self.real_endpose}")
            self.real_endpose_pub.publish(self.real_endpose)
            self.endflag=False
def main(args=None):
    rclpy.init(args=args)
    node = YoloCmdNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()