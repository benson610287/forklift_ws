#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, Int32
import time
import math


class TestGoalPublisher(Node):
    def __init__(self):
        super().__init__('test_goal_publisher')
        
        # 發布目標位姿到 pose_navigation_node
        self.goal_publisher = self.create_publisher(
            Float32MultiArray,
            '/timda_nav_pose',
            10
        )
        
        # 訂閱導航成功回饋
        self.nav_success_subscriber = self.create_subscription(
            Int32,
            '/timda_nav_success',
            self.nav_success_callback,
            10
        )
        
        # 測試狀態追蹤
        self.current_goal_index = 0
        self.test_start_time = None
        
        # 簡單的兩點測試 [x, y, angle_degrees]
        self.test_goals = [
            [1.0, 0.0, 0.0],      # 第一個目標點
            [0.0, 1.0, 90.0],     # 第二個目標點
        ]
        
        self.get_logger().info('Pose Navigation 測試節點啟動')
        self.get_logger().info(f'測試目標: 點1({self.test_goals[0][0]}, {self.test_goals[0][1]}, {self.test_goals[0][2]}°)')
        self.get_logger().info(f'         點2({self.test_goals[1][0]}, {self.test_goals[1][1]}, {self.test_goals[1][2]}°)')
        
        self.start_test()
    
    def start_test(self):
        """開始兩點測試"""
        self.get_logger().info('開始兩點導航測試')
        self.current_goal_index = 0
        self.send_next_goal()
    
    def send_next_goal(self):
        """發送下一個測試目標"""
        if self.current_goal_index < len(self.test_goals):
            goal = self.test_goals[self.current_goal_index]
            self.get_logger().info(f'發送目標 {self.current_goal_index + 1}/{len(self.test_goals)}: X={goal[0]}, Y={goal[1]}, 角度={goal[2]}°')
            
            # 發布目標位姿
            msg = Float32MultiArray()
            msg.data = [float(goal[0]), float(goal[1]), float(goal[2])]
            self.goal_publisher.publish(msg)
            
            self.test_start_time = time.time()
        else:
            self.get_logger().info('🎉 兩點測試完成！')
    
    def nav_success_callback(self, msg):
        """處理導航成功回饋"""
        if msg.data == 1:
            elapsed_time = time.time() - self.test_start_time if self.test_start_time else 0
            self.get_logger().info(f'目標 {self.current_goal_index + 1} 導航成功！耗時: {elapsed_time:.1f} 秒')
            
            # 移動到下一個目標
            self.current_goal_index += 1
            if self.current_goal_index < len(self.test_goals):
                self.get_logger().info('發送下一個目標...')
                self.send_next_goal()
                self.get_logger().info('🎉 所有測試完成！')
                
        elif msg.data == 2:
            elapsed_time = time.time() - self.test_start_time if self.test_start_time else 0
            self.get_logger().warn(f'❌ 目標 {self.current_goal_index + 1} 導航失敗！耗時: {elapsed_time:.1f} 秒')
            self.get_logger().info('測試中止')


def main(args=None):
    rclpy.init(args=args)
    
    try:
        node = TestGoalPublisher()
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\n程式被用戶中斷")
    finally:
        rclpy.shutdown()


if __name__ == '__main__':
    main()