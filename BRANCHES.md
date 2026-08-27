# Branch 說明 — 每個分支負責什麼

> 簡單版說明，讓新成員快速知道每個 branch 的用途。
> 所有內容已整合進 **`integration`**（準備成為新的 main），舊分支僅供查歷史。

## 分支總覽

| Branch | 負責人/用途 | 主要內容 | 狀態 |
|---|---|---|---|
| `integration` | 全部整合 | 所有分支功能 + 單一 Docker image + 完整 README | ✅ 最新，用這個 |
| `main` | 舊的整合主幹（2025-10-17） | 各子系統當時最新版 | 已被 integration 取代 |
| `benson` | GUI / 主控 | 修 GUI 關閉當掉問題、main_control 更新、shelf docking | 已併入 |
| `glenn` | 棧板對接 docking | docking 控制器（Yolo 深度 → RANSAC → PID）、launch 檔 | 已併入 |
| `taiwen` | 棧板堆疊 pallet | YOLO 箱子偵測、box pose 發布、PalletMain 流程 | 已併入 |
| `zack` | 貨架偵測 shelf | ArUco 貨架姿態估測（shelf_pose_est）、YOLO 模型、docker_shelf | 已併入 |
| `weng` | 棧板監控 | pallet_monitor 架構、整合 taiwen+benson 的 pallet 修改 | 已併入 |
| `hungyu` | 光達 | timda_bringup 光達修正（fix lidar）、README | 已併入 |
| `jinghua` | 文件 | README 更新、小修 | 已併入 |
| `all_forklift` | 三台機器快照（2025-11-26） | 機器上實際跑的最終版程式（見下方） | 重要部分已併入 |

## 各分支細節：主要 node 與工作

### benson — GUI / 主控制
- `gui main`（PyQt5 操作介面）：修掉關閉視窗時程式當掉的問題（thread flag + `app.exit()`）。
- `main_control main`（任務調度器）：接 `/taskcmd` 服務，依序執行 slam → parking → docking → shelf_docking 等任務。
- 也加了早期的 shelf docking。

### glenn — 棧板對接（docking）
- `YoloDepthProcessor`：YOLO 偵測棧板 + 深度 → 發布點雲。
- `ransac`：從點雲擬合棧板平面，發布 `/plane_center`、`/plane_normal`。
- `pid_mecanum_node`：用平面誤差做 PID，控制底盤對準棧板。
- 貢獻了 `docking_nodes.launch.py`（一鍵啟動上面三個 node）。

### taiwen — 棧板堆疊（pallet）
- `get_box_from_yolo`：YOLOv8 偵測箱子位置。
- `PalletMain`：堆疊主流程，服務 `Pallet`，控制手臂夾箱、疊棧板。
- box pose 發布（給手臂用的箱子姿態）。

### zack — 貨架偵測（shelf）
- `shelf_pose`（aruco_detect）：ArUco marker（id 0–7）估貨架姿態，發布 PoseArray，服務 `/toggle_aruco_detection` 開關。
- `aruco_offset_forklift`：同上的變體，用堆高機上的相機 + 位置偏移。
- YOLO 貨架模型、`docker_shelf` 環境。
- 注意：這個分支只做「偵測」，實際移動的 `shelf_docking` 在 main。

### weng — 棧板監控（pallet_monitor）
- `pallet_monitoring` pipeline：獨立的棧板監控流程（目前是 mock 架構）。
- 把 taiwen 和 benson 的 pallet 修改合在一起。

### hungyu / jinghua — 光達與文件
- hungyu：`timda_bringup` 的光達 launch 修正（雙 Hokuyo URG）。
- jinghua：README 補充。

### all_forklift — 三台機器的最終快照（很重要）
比 main 晚一個月，是機器上「實際在跑」的版本：
- `forkliftdocking_ws`（對接機）：`aruco_parking_node` 改成 `/parking` 服務版（精準停車）、`docking_status_server` 多執行緒版 → **已併入 integration**。
- `forkliftslam_ws`（SLAM 機）：新版 `timda_slam`（`pose_navigation_node` 收 `/timda_nav_pose`、`change_map` 換地圖）、`forklift_urdf` 車體模型 → **已併入 integration**。
- `forklift_ws`（主機）：與 main 大致相同，無新東西。

### integration — 最終整合（新 main）
- 上面所有功能 + `docker_all/docker_unified/`（一個 image 裝全部依賴）+ 完整 README 啟動手冊。
- 怎麼啟動每個 node → 看 [README.md](README.md) 第 3 節。
