from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='docking_pkg',
            executable='YoloDepthProcessor',
            name='yolo_depth_processor',
            output='screen'
        ),
        Node(
            package='docking_pkg',
            executable='ransac',
            name='ransac_node',
            output='screen'
        ),
        Node(
            package='docking_pkg',
            executable='pid_mecanum_node',  # 如果是 Python script，請確認 setup.py 有正確設定 entry_point
            name='pid_mecanum_node',
            output='screen'
        ),
    ])
