#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray, Int32
from nav2_simple_commander.robot_navigator import BasicNavigator,TaskResult
import tf2_ros
from tf2_geometry_msgs import do_transform_pose
import math


class PoseNavigationNode(Node):
    def __init__(self):
        super().__init__('pose_navigation_node')
        
        # 初始化 nav2 navigator
        self.navigator = BasicNavigator()
        
        # 導航狀態追蹤
        self.is_navigating = False
        self.current_goal = None
        
        # 創建訂閱者，接收目標位姿 (x, y, qz, qw)
        self.pose_subscriber = self.create_subscription(
            Float32MultiArray,
            '/timda_nav_pose',
            self.pose_callback,
            10
        )
        
        # 創建發布者，在導航成功時發布數值 1
        self.nav_success_publisher = self.create_publisher(
            Int32,
            '/timda_nav_success',
            10
        )
        
        # 創建定時器來檢查導航狀態 (非阻塞)
        self.nav_check_timer = self.create_timer(1.0, self.check_navigation_status)
        
        # TF2 buffer 和 listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        self.get_logger().info('Pose Navigation Node initialized - waiting for [x, y, angle_degrees] messages')
        
        # 等待 nav2 準備就緒
        self.navigator.waitUntilNav2Active()
        self.get_logger().info('Nav2 is active')
        
        # 設置初始點位
        self.set_initial_pose()
    
    def set_initial_pose(self):
        """設置機器人的初始點位"""
        try:
            initial_pose = PoseStamped()
            initial_pose.header.frame_id = 'map'
            initial_pose.header.stamp = self.get_clock().now().to_msg()
            
            # 設置初始位置 (可根據實際環境調整)
            initial_pose.pose.position.x = 0.0
            initial_pose.pose.position.y = 0.0
            initial_pose.pose.position.z = 0.0
            
            # 設置初始方向 (面向 x 正方向)
            initial_pose.pose.orientation.x = 0.0
            initial_pose.pose.orientation.y = 0.0
            initial_pose.pose.orientation.z = 0.0
            initial_pose.pose.orientation.w = 1.0
            
            # 設置初始位姿
            self.navigator.setInitialPose(initial_pose)
            self.get_logger().info('Initial pose set: x=0.0, y=0.0, qz=0.0, qw=1.0')
            
        except Exception as e:
            self.get_logger().error(f'Failed to set initial pose: {str(e)}')
    
    def pose_callback(self, msg):
        """接收 x, y, angle_degrees 並導航到該位姿 (非阻塞)"""
        if len(msg.data) != 3:
            self.get_logger().error(f'Expected 3 values [x, y, angle_degrees], got {len(msg.data)}')
            return
        
        # 如果正在導航，先取消當前任務
        if self.is_navigating:
            self.get_logger().info('Canceling current navigation task')
            self.navigator.cancelTask()
            self.is_navigating = False
        
        x, y, angle_degrees = msg.data

        # 將角度從度數轉換為弧度
        angle_radians = math.radians(-angle_degrees)

        # 將角度轉換為四元數 (只繞 z 軸旋轉)
        qz = math.sin(angle_radians / 2.0)
        qw = math.cos(angle_radians / 2.0)

        self.get_logger().info(f'Received goal: x={x:.2f}, y={y:.2f}, angle={angle_degrees:.1f}° (qz={qz:.4f}, qw={qw:.4f})')
        
        try:
            # 創建 PoseStamped 訊息
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.get_clock().now().to_msg()
            
            # 設定位置
            goal_pose.pose.position.x = float(x)
            goal_pose.pose.position.y = float(y)
            goal_pose.pose.position.z = 0.0
            
            # 直接使用四元數分量
            goal_pose.pose.orientation.x = 0.0
            goal_pose.pose.orientation.y = 0.0
            goal_pose.pose.orientation.z = float(qz)
            goal_pose.pose.orientation.w = float(qw)
            
            # 啟動導航 (非阻塞)
            self.navigator.goToPose(goal_pose)
            self.is_navigating = True
            self.current_goal = goal_pose
            
            self.get_logger().info('Navigation started (non-blocking)')

        except Exception as e:
            self.get_logger().error(f'Navigation error: {str(e)}')
            self.is_navigating = False
    
    def check_navigation_status(self):
        """定時檢查導航狀態 (由定時器調用，非阻塞)"""
        if not self.is_navigating:
            return
        
        # 檢查導航是否完成
        if self.navigator.isTaskComplete():
            result = self.navigator.getResult()
            
            if result == TaskResult.SUCCEEDED:
                self.get_logger().info('Navigation succeeded!')
                # 發布導航成功訊息
                success_msg = Int32()
                success_msg.data = 1
                self.nav_success_publisher.publish(success_msg)
                self.get_logger().info('Published navigation success signal: 1')
                
            elif result == TaskResult.CANCELED:
                self.get_logger().warn('Navigation was canceled')
                success_msg = Int32()
                success_msg.data = 2
                self.nav_success_publisher.publish(success_msg)
                self.get_logger().info('Published navigation success signal: 2')
            elif result == TaskResult.FAILED:
                self.get_logger().error('Navigation failed')
                success_msg = Int32()
                success_msg.data = 2
                self.nav_success_publisher.publish(success_msg)
                self.get_logger().info('Published navigation success signal: 2')
                
            
            # 重置導航狀態
            self.is_navigating = False
            self.current_goal = None
            


def main(args=None):
    rclpy.init(args=args)
    node = PoseNavigationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()