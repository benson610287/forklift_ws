#!/bin/bash
echo "=== 旋轉測試腳本 ==="

echo "開始監控里程計角度..."
echo "請手動旋轉機器人360度，然後按Ctrl+C停止"

# 監控odom話題的角度變化
ros2 topic echo /odom/pose/pose/orientation | while read line; do
    if [[ $line == *"z:"* ]]; then
        z_val=$(echo $line | grep -o '[0-9.-]\+')
        # 將四元數z分量轉換為角度（簡化）
        angle_deg=$(echo "scale=2; $z_val * 180 / 3.14159 * 2" | bc)
        echo "當前角度(度): $angle_deg"
    fi
done