from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace

def generate_launch_description():
    return LaunchDescription([
        GroupAction([
            PushRosNamespace("pallet_monitoring"),

            Node(
                package='pallet_monitoring',
                executable='pub',
                name='image_publisher'
            ),

            Node(
                package='pallet_monitoring',
                executable='yolo',
                name='pallet_yolo_detector'
            ),

            Node(
                package='pallet_monitoring',
                executable='cropper',
                name='pallet_cropper'
            ),

            Node(
                package='pallet_monitoring',
                executable='clutter',
                name='pallet_clutter_evaluator'
            ),

            Node(
                package='pallet_monitoring',
                executable='decision',
                name='pallet_decision'
            ),
        ])
    ])
