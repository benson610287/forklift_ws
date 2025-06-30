# TIMDA 機器人導航系統

本套件提供基於 Nav2、AMCL 的 ROS2 機器人導航解決方案，支援地圖定位、路徑規劃與目標點導航，並額外提供 topic 方式直接導航到指定點位。

---



## 安裝與建置
```bash
cd /path/to/your/workspace
colcon build --packages-select timda_slam
source install/setup.bash
```
##開啟底盤與光達
ros2 launch timda_bringup urg_lidar.launch.py 
ros2 run mecanum mobile_node 
## 開啟rviz
本功能包有提供rviz.rviz設定檔
## SLAM 建圖教學

本章節說明如何使用 timda_slam 內建的 slam_toolbox 啟動檔進行地圖建構（SLAM建圖）。

### 1. 啟動 SLAM 建圖節點
請使用本套件內建的啟動檔啟動slam建圖：
```bash
ros2 launch timda_slam online_async.launch.py
```
- 如需自訂參數（如雷射topic、參數檔），可參考launch檔內說明或自行修改。

### 2. 遙控機器人移動
使用遙控器、鍵盤或其他方式讓機器人行走，讓雷射掃描覆蓋整個環境。

### 3. 儲存地圖
建圖完成後，可使用slam_toolbox內建service或map_saver_cli儲存地圖：
- 使用service儲存（推薦，RViz可直接呼叫）：
  1. 在RViz點擊「Save Map」按鈕，或
  2. 執行以下指令：
     ```bash
     ros2 service call /slam_toolbox/save_map slam_toolbox/srv/SaveMap "{name: '/path/to/save/map'}"
     ```
- 或用map_saver_cli：
     ```bash
     ros2 run nav2_map_server map_saver_cli -f ~/map
     ```
- 會產生 `map.pgm` 及 `map.yaml` 兩個檔案。

### 4. 地圖檔案放置
將產生的地圖檔案複製到 `src/timda_slam/maps/` 目錄下，供導航系統使用。

---
---

## 地圖準備
將地圖檔案放入 `src/timda_slam/maps/` 目錄：
- `map.pgm`：地圖影像
- `map.yaml`：地圖描述
並Colconbuild
---

## 啟動導航/定位

### 啟動完整導航系統
```bash
ros2 launch timda_slam navigation.launch.py
```


### 使用自定義地圖
```bash
ros2 launch timda_slam navigation.launch.py map:=/path/to/your/map.yaml
```

---
## RViz 操作說明
1. 啟動 RViz，載入地圖與導航模組
2. 設定初始位姿：
   - 使用「2D Pose Estimate」工具
   - 在地圖上點擊並拖曳設置機器人初始位置與朝向
3. 設定導航目標：
   - 使用「Nav2 Goal」工具
   - 在地圖上點擊設置目標點

---
## 導航到點位 (Topic 控制)

###面向貨價那面牆時為0度

本套件提供 `/goal_pose_simple` topic，可直接以訊息控制機器人導航到指定 (x, y, yaw) 地圖座標。

### 啟動 pose navigation node
```bash
ros2 run timda_slam pose_navigation_node
```

### 手動發布目標位姿 (x, y, yaw)
```bash
ros2 topic pub /goal_pose_simple std_msgs/msg/Float32MultiArray '{data: [2.0, 1.0, 0.0]}' --once
```
- 例：移動到 (-1, 1.5) 並面向 90 度
```bash
ros2 topic pub /goal_pose_simple std_msgs/msg/Float32MultiArray '{data: [-1, 1.5, 90]}' --once
```



### Topic 格式說明
- Topic 名稱：`/goal_pose_simple`
- 訊息型別：`std_msgs/Float32MultiArray`
- 資料內容：`[x, y, yaw]` (單位：公尺, 弧度)
- 參考座標系：`map`

---



## 參數調整建議
- 定位不穩定：
  - 增加 `max_particles` (如3000)
  - 降低 `alpha1-5` 運動噪聲
  - 調整 `laser_likelihood_max_dist`
- 定位響應慢：
  - 降低 `update_min_d`、`update_min_a`
  - 增加 `recovery_alpha_fast`

---

## 常見問題排查
1. **機器人不動**：檢查 `cmd_vel` 話題是否正確發布
2. **定位漂移**：確認 TF 變換正確，特別是 `odom`→`base_link`
3. **雷射不匹配**：檢查 `scan` 話題與座標系
4. **路徑規劃失敗**：確認地圖正確加載，costmap 參數合理

---

## 依賴項
- rclpy
- geometry_msgs
- std_msgs
- nav2_simple_commander
- tf2_ros
- tf2_geometry_msgs
- nav2_bringup
- nav2_amcl
- nav2_map_server
- nav2_lifecycle_manager
- nav2_controller
- nav2_planner
- nav2_behaviors
- nav2_bt_navigator
- nav2_costmap_2d
- nav2_smoother
- nav2_waypoint_follower
- nav2_velocity_smoother
- nav2_collision_monitor
- nav2_mppi_controller
- nav2_navfn_planner
- launch
- launch_ros
- rviz2
- tf2
- sensor_msgs
- nav_msgs

## 配置說明

## 故障排除

1. **機器人不動**：檢查`cmd_vel`話題是否正確發布
2. **定位漂移**：確認TF變換正確，特別是`odom`→`base_link`
3. **激光不匹配**：檢查`scan`話題和坐標系配置
4. **路徑規劃失敗**：確認地圖正確加載，costmap參數合理

## 依賴項

- nav2_bringup
- nav2_amcl  
- nav2_map_server
- nav2_controller
- nav2_planner
- 其他Nav2相關包 
