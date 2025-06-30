#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import Float32MultiArray
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import tf2_ros
from tf2_geometry_msgs import do_transform_pose
import math


class PoseNavigationNode(Node):
    def __init__(self):
        super().__init__('pose_navigation_node')
        
        # 初始化 nav2 navigator
        self.navigator = BasicNavigator()
        
        # 創建訂閱者，接收目標位姿 (x, y, yaw)
        self.pose_subscriber = self.create_subscription(
            Float32MultiArray,
            '/Timda_pose',
            self.pose_callback,
            10
        )
        
        # TF2 buffer 和 listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        
        self.get_logger().info('Pose Navigation Node initialized - waiting for [x, y, yaw] messages')
        
        # 等待 nav2 準備就緒
        self.navigator.waitUntilNav2Active()
        self.get_logger().info('Nav2 is active')
    
    def pose_callback(self, msg):
        """接收 x, y, yaw 並導航到該位姿"""
        if len(msg.data) != 3:
            self.get_logger().error(f'Expected 3 values [x, y, yaw], got {len(msg.data)}')
            return
        self.navigator.cancelTask()
        x, y, yaw = msg.data
        # 將角度轉為弧度
        yaw = math.radians(yaw-104.68)
        self.get_logger().info(f'Received goal: x={x:.2f}, y={y:.2f}, yaw={yaw:.2f} (radian)')
        
        try:
            # 創建 PoseStamped 訊息
            goal_pose = PoseStamped()
            goal_pose.header.frame_id = 'map'
            goal_pose.header.stamp = self.get_clock().now().to_msg()
            
            # 設定位置
            goal_pose.pose.position.x = float(x)
            goal_pose.pose.position.y = float(y)
            goal_pose.pose.position.z = 0.0
            
            # 轉換 yaw 角度到四元數
            goal_pose.pose.orientation.x = 0.0
            goal_pose.pose.orientation.y = 0.0
            goal_pose.pose.orientation.z = math.sin(yaw / 2.0)
            goal_pose.pose.orientation.w = math.cos(yaw / 2.0)
            
            # 導航到目標位姿
            self.navigator.goToPose(goal_pose)
            
            # 等待導航完成
            while not self.navigator.isTaskComplete():
                rclpy.spin_once(self, timeout_sec=0.1)
            
            # 檢查導航結果
            result = self.navigator.getResult()
            if result == BasicNavigator.TaskResult.SUCCEEDED:
                self.get_logger().info('Navigation succeeded!')
            elif result == BasicNavigator.TaskResult.CANCELED:
                self.get_logger().warn('Navigation was canceled')
            elif result == BasicNavigator.TaskResult.FAILED:
                self.get_logger().error('Navigation failed')
            
            # 每次導航結束後重置 Navigator 狀態，確保能接受新目標

        except Exception as e:
            self.get_logger().error(f'Navigation error: {str(e)}')


def main(args=None):
    rclpy.init(args=args)
    node = PoseNavigationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()