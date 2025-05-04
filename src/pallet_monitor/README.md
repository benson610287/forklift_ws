# Pallet Monitor (ROS2)

A modular ROS2-based pallet inspection pipeline that detects and evaluates cluttered pallets using simulated YOLO detection, image cropping, clutter scoring, and decision-making.

This project is a submodule of a larger system. It includes two tightly coupled ROS2 packages grouped together under the `pallet_monitoring` directory for easier version control and branching.

---

## System Overview

This system is composed of 5 key nodes:

1. **Image Publisher**: Publishes a static test image to `image`
2. **YOLO Detector (mock)**: Simulates object detection and publishes pallet bounding boxes to `yolo_result`
3. **Pallet Cropper**: Simulates cropping images based on bounding boxes and publishes them to `cropped_pallets`
4. **Clutter Evaluator**: Simulates evaluating how cluttered each pallet is and publishes results to `clutter_evaluations`
5. **Decision Maker**: Processes evaluation results and publishes actions to `result`

All nodes run under the ROS2 namespace: `pallet_monitoring`

---

## Package Structure

```
pallet_monitor/
├── interfaces/                # Custom message definitions (ament_cmake)
│   ├── msg/
│   │   ├── PalletBBox.msg
│   │   ├── PalletBBoxArray.msg
│   │   ├── CroppedPallet.msg
│   │   ├── CroppedPalletArray.msg
│   │   ├── ClutterEvaluation.msg
│   │   ├── ClutterEvaluationArray.msg
│   │   ├── PalletAction.msg
│   │   └── PalletMonitoringResult.msg
│   ├── CMakeLists.txt
│   ├── package.xml
│   └── src/
├── pallet_monitoring/        # Python node implementations (ament_python)
│   ├── pallet_monitoring/
│   │   ├── __init__.py
│   │   ├── img_pub.py
│   │   ├── pallet_yolo_detector.py
│   │   ├── pallet_cropper.py
│   │   ├── pallet_clutter_evaluator.py
│   │   └── pallet_decision.py
│   ├── img/test_image.jpg
│   ├── launch/pallet_monitoring.launch.py
│   ├── setup.py
│   ├── setup.cfg
│   └── package.xml
```

---

## How to Build & Run

### 1. Build the Workspace

```bash
colcon build --symlink-install
source install/setup.bash
```

### 2. Launch the System

```bash
ros2 launch pallet_monitoring pallet_monitoring.launch.py
```

This will launch all 5 nodes under the namespace `/pallet_monitoring`.

---

## Topics

| Topic Name                               | Type                     | Description                     |
| ---------------------------------------- | ------------------------ | ------------------------------- |
| `/pallet_monitoring/image`               | `sensor_msgs/Image`      | Raw test image                  |
| `/pallet_monitoring/yolo_result`         | `PalletBBoxArray`        | Simulated YOLO BBox results     |
| `/pallet_monitoring/cropped_pallets`     | `CroppedPalletArray`     | Simulated cropped pallet images |
| `/pallet_monitoring/clutter_evaluations` | `ClutterEvaluationArray` | Simulated clutter scores        |
| `/pallet_monitoring/result`              | `PalletMonitoringResult` | Final action decisions          |

---

## Message Definitions

### `PalletBBox.msg`
Bounding box info from YOLO:
- `int32 id`
- `float32 x_min, y_min, x_max, y_max`
- `float32 confidence`
- `string class_label`

### `PalletBBoxArray.msg`
- `std_msgs/Header header`
- `PalletBBox[] bboxes`

### `CroppedPallet.msg`
- `int32 id`
- `sensor_msgs/Image cropped_image`

### `CroppedPalletArray.msg`
- `std_msgs/Header header`
- `CroppedPallet[] pallets`

### `ClutterEvaluation.msg`
- `int32 pallet_id`
- `float32 clutter_score`
- `bool needs_sorting`
- `float32 confidence`

### `ClutterEvaluationArray.msg`
- `std_msgs/Header header`
- `ClutterEvaluation[] evaluations`

### `PalletAction.msg`
- `int32 pallet_id`
- `string action_type`  (e.g., "sort", "ignore")
- `string reason`
- `float32 score`

### `PalletMonitoringResult.msg`
- `std_msgs/Header header`
- `PalletAction[] actions`

