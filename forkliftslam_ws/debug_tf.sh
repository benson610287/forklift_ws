#!/bin/bash

echo "=== SLAM TF 調試腳本 ==="
echo ""

echo "1. 檢查當前 TF 樹..."
echo "   執行中... (等待5秒收集TF數據)"
timeout 5s rostopic echo /tf --noarr > tf_output.txt 2>&1 &
sleep 6

echo ""
echo "2. 檢查重要話題..."
echo "   檢查 /scan_multi 話題:"
timeout 2s rostopic echo /scan_multi/header -n 1 2>/dev/null | grep -E "(frame_id|stamp)" || echo "   ❌ /scan_multi 話題不可用"

echo ""
echo "   檢查 /odom 話題:"
timeout 2s rostopic echo /odom/header -n 1 2>/dev/null | grep -E "(frame_id|stamp)" || echo "   ❌ /odom 話題不可用"

echo ""
echo "3. 檢查 TF 變換..."
echo "   檢查 map -> base_link 變換:"
rosrun tf tf_echo map base_link 2>/dev/null | head -10 || echo "   ❌ map -> base_link 變換不可用"

echo ""
echo "   檢查 odom -> base_link 變換:"
rosrun tf tf_echo odom base_link 2>/dev/null | head -10 || echo "   ❌ odom -> base_link 變換不可用"

echo ""
echo "   檢查 base_link -> laser_merged 變換:"
rosrun tf tf_echo base_link laser_merged 2>/dev/null | head -10 || echo "   ❌ base_link -> laser_merged 變換不可用"

echo ""
echo "4. 生成 TF 樹圖..."
rosrun tf view_frames 2>/dev/null && echo "   ✅ TF 樹圖已生成 (frames.pdf)" || echo "   ❌ 無法生成 TF 樹圖"

echo ""
echo "5. 檢查節點狀態..."
echo "   SLAM 節點:"
rosnode info /slam_toolbox 2>/dev/null >/dev/null && echo "   ✅ slam_toolbox 運行中" || echo "   ❌ slam_toolbox 未運行"

echo "   移動底盤節點:"
rosnode info /mobile_node 2>/dev/null >/dev/null && echo "   ✅ mobile_node 運行中" || echo "   ❌ mobile_node 未運行"

echo "   激光合併節點:"
rosnode info /laserscan_multi_merger 2>/dev/null >/dev/null && echo "   ✅ laserscan_multi_merger 運行中" || echo "   ❌ laserscan_multi_merger 未運行"

echo ""
echo "=== 調試完成 ==="
echo ""
echo "建議解決方案:"
echo "1. 如果 map -> base_link 變換不可用，檢查 SLAM 是否正常啟動"
echo "2. 如果 odom -> base_link 變換不可用，檢查 mobile_node 是否運行"
echo "3. 如果時間戳不同步，可能需要重啟所有節點"
echo "4. 檢查 /scan_multi 的 frame_id 是否為 'laser_merged'" 