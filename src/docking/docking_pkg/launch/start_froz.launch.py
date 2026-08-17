from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration , PathJoinSubstitution


from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='docking_pkg',
            executable='docking_status_server',
            output='screen',
            name='docking_status_server'
        ),
        Node(
            package='docking_pkg',
            executable='YoloDepthProcessor',
            output='screen',
            name='YoloDepthProcessor'
        ),
        Node(
            package='docking_pkg',
            executable='ransac',
            output='screen',
            name='ransac',
        ),
        Node(
            package='docking_pkg',
            executable='pid_mecanum_node',
            output='screen',
            name='pid_mecanum_node'
        ),
        Node(
            package='docking_pkg',
            executable='aruco_parking_node',
            output='screen',
            name='aruco_parking_node'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('realsense2_camera'),
                    'launch',
                    'rs_launch.py'
                ])
            ]),
            launch_arguments={
                'serial_no': "'844212070219'",
                'rgb_camera.color_profile': '640x480x30',
            }.items()
        ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([
        #         PathJoinSubstitution([
        #             FindPackageShare('ur_moveit_config'),
        #             'launch',
        #             'ur_moveit.launch.py'
        #         ])
        #     ]),
        #     launch_arguments={
        #         'ur_type': 'ur5e',
        #         'use_fake_hardware': 'false',
        #         'launch_rviz': 'true'
        #     }.items()
        # ),
        
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource([
        #         PathJoinSubstitution([
        #             FindPackageShare('realsense2_camera'),
        #             'launch',
        #             'rs_launch.py'
        #         ])
        #     ]),
        #     launch_arguments={
        #         'align_depth.enable': 'true',
        #         'serial_no': "'844212070148'",
        #         'camera_name': 'Armcamera',
        #         'rgb_camera.color_profile': '1920x1080x30'
        #     }.items()
        # ),
    ])