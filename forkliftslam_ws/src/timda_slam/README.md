# TIMDA 機器人導航系統

本套件提供基於 Nav2、AMCL 的 ROS2 機器人導航解決方案，支援地圖定位、路徑規劃與目標點導航，並額外提供 topic 方式直接導航到指定點位。

---

## 安裝與建置
```bash
cd /path/to/your/workspace
colcon build --packages-select timda_slam
source install/setup.bash
```
啟動docker
```bash 
./home/flash/forkliftslam_ws/docker_all/docker_hyslam/run.sh
```
##開啟底盤與光達
```bash
source install/setup.bash 
ros2 launch timda_bringup urg_lidar.launch.py 
ros2 run mecanum mobile_node 
sudo chmod 777 /dev/ttyUSB0 /dev/ttyUSB1
ros2 run linear_move slide 
ros2 run keyboard_control main
```
## 開啟rviz
本功能包有提供rviz.rviz設定檔
在src/timda_slam/rviz.rviz



## 啟動導航/定位

### 啟動導航系統
```bash
ros2 launch timda_slam navigation.launch.py pose_navigation:=False
```
#### 使用 RViz2 手動導航 操作說明
1. 啟動 RViz，載入地圖與導航模組
2. 設定初始位姿：
   - 使用「2D Pose Estimate」工具
   - 在地圖上點擊並拖曳設置機器人初始位置與朝向
   - 使出現的costmap虛影盡量與地圖重疊 可以多拉幾次
3. 設定導航目標：
   - 使用「Nav2 Goal」工具
   - 在地圖上點擊設置目標點
   
#### 使用TOPIC導航到點位

### 啟動 pose navigation node
在上述導航系已啟動的的情情況下

```bash
ros2 run timda_slam pose_navigation_node

```
### 設置初始點位(如果是由起點出發可以忽略這步)
   - 節點啟動時會動將將0,0,0(起點 )設為初始點位 如果不是在起點啟動 則建議使用rviz2手動發布起點
   - 使用「2D Pose Estimate」工具
   - 在地圖上點擊並拖曳設置機器人初始位置與朝向
   - 使出現的costmap虛影盡量與地圖重疊 可以多拉幾次
或是在topic發布 
ros2 topic pub /initialpose geometry_msgs/PoseWithCovarianceStamped '{header: {frame_id: "map"}, pose: {pose: {position: {x: 你的X座標, y: 你的Y座標, z: 0.0}, orientation:(你的角度四元數) {x: ?, y: ?, z: ?, w: ?}}}}' --once


本套件提供 `/timda_nav_pose` topic，可直接以訊息控制機器人導航到指定 (x, y, yaw) 地圖座標。

### 使用TOPIC發布導航終點座標 (x, y, yaw)
##先去RIVZ2使用Publish Point工具 滑鼠指向地圖上的點位，x,y座標會顯示在左下角，找到目標點位之x,y座標後yam之角度直接目測，面向研究生座位區，與場地周圍平行為0度
```bash
ros2 topic pub /timda_nav_pose std_msgs/msg/Float32MultiArray '{data: [2.0, -1.0, 90.0]}' --once
ros2 topic pub /timda_nav_pose std_msgs/msg/Float32MultiArray '{data: [3.0, -1.0, 0.0]}' --once
```
導航完成後 /timda_nav_success 會回傳一個int 1以回報導航順利完成 ,2為發生錯誤 


---


## SLAM 建圖教學

本章節說明如何使用 timda_slam 內建的 slam_toolbox 啟動檔進行地圖建構（SLAM建圖）。
ros2 topic pub /initialpose geometry_msgs/PoseWithCovarianceStamped '{header: {frame_id: "map"}, pose: {pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}}' --once
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


