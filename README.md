# TIMDA Forklift AMR 自主堆高機

ROS 2 Humble autonomous forklift: mecanum-wheel base, linear fork lift, dual Hokuyo lidar (SLAM + Nav2), UR5e arm (MoveIt), RealSense + Azure Kinect cameras, YOLOv8 pallet detection, ArUco shelf docking.

| Subsystem | Package(s) | Hardware |
|---|---|---|
| Mobile base 底盤 | `mecanum` | Orientalmotor BLV over Modbus (`/dev/ttyUSB*`) |
| Fork lift 升降 | `linear_move` | linear axis motor |
| Lidar / SLAM 建圖導航 | `timda_bringup`, `timda_slam`, `ira_laser_tools` | 2× Hokuyo URG (`/dev/ttyACM0/1`) |
| Arm 手臂 | `arm_control` (moveit_driver + UR driver) | UR5e @ `192.168.56.10` |
| Pallet 棧板堆疊 | `pallet` (pallet_main, pallet_model) | RealSense `Armcamera` |
| Shelf docking 貨架對接 | `shelf` (shelf_pose_est, shelf_docking) | RealSense / Azure Kinect |
| Pallet docking 棧板對接 | `docking` (docking_pkg) | RealSense |
| Orchestration + UI 控制與介面 | `main_control`, `GUI`, `interface` | — |
| Monitoring 監控 | `pallet_monitor` | — |

---

## 1. Environment Setup (Docker) 環境建置

Host prep (once per boot) — serial device permissions:

```bash
./start.sh                      # chmod /dev/ttyUSB0 /dev/ttyUSB1
source cyclonedds_config.sh     # ROS_DOMAIN_ID=42 + CycloneDDS (optional on host)
```

Build and enter the **unified container** (one image for the whole stack):

```bash
./docker_all/docker_unified/build.sh   # first time only (large: CUDA + ROS + torch)
./docker_all/docker_unified/run.sh     # opens terminator; repo mounted at ~/work
```

The container runs privileged with host network; all `/dev` devices are visible. Open more shells inside terminator with right-click → split (or `docker exec -it unified bash`).

> **GPU note:** the image is based on CUDA 12.8 — the host needs NVIDIA driver **≥ 550** (`nvidia-smi` to check).

Legacy per-subsystem images `docker_ros2` / `docker_hyslam` / `docker_pallet` / `docker_shelf` are **deprecated** — kept temporarily, use `docker_unified` instead.

## 2. Build 編譯

Inside the container, at `~/work`:

```bash
rosdep install --from-paths src --ignore-src -r -y   # first time
colcon build
source install/setup.bash    # ⚠ every new terminal
```

## 3. Full-Stack Launch Runbook 全系統啟動流程

One command per terminal/pane, **in this order** (`source install/setup.bash` first in each):

```bash
# ① Base hardware: mecanum base + fork lift + dual lidar + scan merger + TF
ros2 launch timda_bringup start_hardware.launch.py

# ② Navigation (needs ① for /scan_multi, /odom, TF)
ros2 launch timda_slam navigation.launch.py            # uses map timda_slam/maps/map.yaml
#    → set initial pose in RViz ("2D Pose Estimate") before sending goals

# ③ Arm + cameras + palletizing + shelf docking
#    (starts UR5e driver, MoveIt, RealSense Armcamera, shelf_pose, shelf_docking,
#     moveit_driver goal servers, PalletMain)
ros2 launch pallet_main start.launch.py

# ④ RL bin-packing planner — REQUIRED, not included in ③
ros2 run pallet_model main

# ⑤ Pallet docking chain
ros2 launch docking_pkg docking_nodes.launch.py        # YoloDepthProcessor + ransac + pid
ros2 run docking_pkg docking_status_server             # separate terminal

# ⑥ Orchestrator (serves /taskcmd; waits for services from ③⑤)
ros2 run main_control main

# ⑦ Operator GUI — or headless auto test
ros2 run gui main
# ros2 run main_control fake_auto        # test driver
# ros2 launch main_control start_main.launch.py   # main + fake_auto together
```

Ordering rules 順序限制:
1. ① before ② — Nav2 will not activate without scan + odom + TF.
2. UR driver + MoveIt before any `moveit_driver` node; `moveit_driver` before `PalletMain` (all inside ③, correct order already).
3. `shelf_pose` must run **and** be enabled (see §5) before `shelf_docking` moves.
4. `linear_move slide` (in ①) before `shelf_docking`.
5. `docking_status_server` before commanding docking.
6. `main_control main` after ③⑤; GUI last.

### Mapping instead of navigation 建圖模式

```bash
ros2 launch timda_slam online_async.launch.py          # slam_toolbox mapping
# drive around (keyboard or cmd_vel), then save:
ros2 run nav2_map_server map_saver_cli -f ~/map
# copy map into src/timda_slam/maps/, then colcon build again
```

Full SLAM/nav details (Chinese): [src/timda_slam/README.md](src/timda_slam/README.md)

## 4. Per-Package Node Reference 節點一覽

| Package | Command | Purpose |
|---|---|---|
| timda_bringup | `ros2 launch timda_bringup start_hardware.launch.py` | base + lift + lidar, all-in-one |
| | `ros2 launch timda_bringup urg_lidar.launch.py` | lidars + merger + robot_state_publisher only |
| mecanum | `ros2 run mecanum mobile_node` | base driver: sub `cmd_vel`, pub `odom` |
| linear_move | `ros2 run linear_move slide` | fork motor, service `linear/move_cmd` |
| keyboard_control | `ros2 run keyboard_control main` | keyboard client for fork |
| timda_slam | `ros2 launch timda_slam navigation.launch.py` | Nav2 + localization + pose_navigation_node |
| | `ros2 launch timda_slam online_async.launch.py` | slam_toolbox mapping |
| | `ros2 run timda_slam pose_navigation_node` | nav goal bridge (`/timda_nav_pose` → Nav2) |
| | `ros2 run timda_slam change_map` | switch maps at runtime |
| | `ros2 run timda_slam test_goal_publisher` | nav test publisher |
| docking_pkg | `ros2 launch docking_pkg docking_nodes.launch.py` | Yolo depth → ransac → pid chain |
| | `ros2 run docking_pkg docking_status_server` | docking service entry (`docking_status_server`) |
| | `ros2 run docking_pkg docking_processor_node` | all-in-one alternative |
| | `ros2 run docking_pkg aruco_parking_node` | ArUco parking control |
| shelf_pose_est | `ros2 run shelf_pose_est shelf_pose` | ArUco shelf pose, service `/toggle_aruco_detection` |
| | `ros2 run shelf_pose_est shelf_pose_offset` | forklift-offset variant — ⚠ same service name, don't run both |
| | `ros2 run shelf_pose_est shelf_state` | shelf state from Azure Kinect depth |
| | `ros2 run shelf_pose_est stream_rs` / `stream_azure` | camera publishers |
| shelf_docking | `ros2 run shelf_docking shelf_docking` | shelf docking control, service `/shelf_docking` |
| pallet_main | `ros2 launch pallet_main start.launch.py` | arm+cameras+palletizing bringup (see ③) |
| | `ros2 run pallet_main PalletMain` | palletizing service `Pallet` |
| | `ros2 run pallet_main get_box_from_yolo` | YOLOv8 box detection |
| pallet_model | `ros2 run pallet_model main` | RL bin-packing planner (required with ③) |
| pallet_monitoring | `ros2 launch pallet_monitoring pallet_monitoring.launch.py` | independent monitor pipeline (mock) |
| moveit_driver | `ros2 run moveit_driver ptop_goal` / `line_goal` / `joint_goal` | arm motion services (need UR driver + MoveIt) |
| main_control | `ros2 run main_control main` | task orchestrator, serves `/taskcmd` |
| | `ros2 run main_control fake_auto` | scripted task test client |
| gui | `ros2 run gui main` | PyQt5 operator UI |

## 5. Service / Topic Triggers 服務指令

```bash
# Send a task to the orchestrator 下任務
ros2 service call /taskcmd gui_interface/srv/Taskcmd "{task: 'palleting'}"
# tasks: slam_parking, parking, palleting, slam_goto_docking, slam_pre_docking,
#        docking, start_positioning, shelf_docking, close_positioning, slam_home

# Enable/disable ArUco detection 開關 ArUco 偵測
ros2 service call /toggle_aruco_detection interface/srv/Maincontroller "{enable: true}"

# Trigger pallet docking directly 直接觸發對接
ros2 service call /docking_status_server interface/srv/Maincontroller "{enable: true}"

# Send a nav goal directly 直接下導航目標 [x, y, yaw°]
ros2 topic pub /timda_nav_pose std_msgs/msg/Float32MultiArray "{data: [2.0, 1.0, 0.0]}" --once

# Move the fork 升降貨叉
ros2 service call linear/move_cmd interface/srv/Slidecmd "{pos: 1000}"
```

## 6. Known Issues 已知問題

- **`parking` task doesn't work**: `main_control` calls a `parking` service but no node serves it (`aruco_parking_node` only publishes `/cmd_vel`).
- **`pallet_model` not in `start.launch.py`** — must be run manually (step ④) or `arm_start_end` never receives an end pose.
- **Don't run `shelf_pose` and `shelf_pose_offset` together** — both serve `/toggle_aruco_detection`.
- `urg_lidar.launch.py` now starts `robot_state_publisher` with `forklift_urdf` — if URDF errors appear on a machine without the arm, comment that node out.
- `mecanum/launch/*.launch` and `timda_gazebo` launch files are **ROS 1 syntax** — not usable under Humble.
- CycloneDDS NIC is pinned to `wlp0s20f3` in `cyclonedds_config.sh` — change to your interface. `ROS_DOMAIN_ID` must match on every machine/container (42 by default; some old notes use 1).
- CUDA 12.8 image needs NVIDIA driver ≥ 550. If `stable_baselines3` PPO model loading fails under new torch (`weights_only` error), load with `torch.load(..., weights_only=False)` or pin torch lower.

---

# GitHub 使用教學

### 第一次使用
```bash
#回到根目錄
$ cd $HOME
#clone工作區
$ git clone https://github.com/benson610287/forklift_ws.git --recursive
#進入工作區
$ cd forklift_ws/
#創建並進入分支
$ git checkout -b $your_brenchname
#加入新創的檔案
$ git add .
#提交檔案
$ git commit -m "version info"
#上傳至該分支的雲端
$ git push -u origin $your_brenchname
```
### 之後使用
```bash
#進入分支
$ git checkout $your_brenchname
#加入新創的檔案
$ git add .
#提交檔案
$ git commit -m "version info"
#上傳至該分支的雲端
$ git push -u origin $your_brenchname
```
