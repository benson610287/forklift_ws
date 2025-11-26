#!/bin/bash
echo "=== ROS2 增強版里程計監控腳本 ==="
echo "檢查話題可用性..."
if ! ros2 topic list | grep -q "/odom"; then echo "❌ /odom 話題不可用"; exit 1; fi
echo "✅ /odom 話題可用，開始監控..."
echo "時間     | 位置(x,y)     | 角度(度) | 說明"
echo "---------------------------------------------"
prev_angle=0
rotation_count=0

# 監控完整的里程計數據
ros2 topic echo /odom nav_msgs/msg/Odometry --field pose.pose.position.x,pose.pose.position.y,pose.pose.orientation.z | while read x; do
  echo "$(date +%H:%M:%S) | 位置和角度數據: $x"
done
