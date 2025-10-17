from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration , PathJoinSubstitution


from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        # Shelf Docking
        Node(
            package='shelf_pose_est',
            executable='shelf_pose',
            output='screen',
            name='shelf_pose'
        ),
        Node(
            package='shelf_docking',
            executable='shelf_docking',
            output='screen',
            name='shelf_docking'
        ),

        # Palleting
        Node(
            package='pallet_main',
            executable='get_box_from_yolo',
            output='screen',
            name='get_box_from_yolo'
        ),
        
        Node(
            package='pallet_main',
            executable='arm_start_end',
            output='screen',
            name='arm_start_end'
        ),
        Node(
            package='pallet_main',
            executable='PalletMain',
            output='screen',
            name='PalletMain'
        ),
        Node(
            package='moveit_driver',
            executable='ptop_goal',
            output='screen',
            name='ptop_goal',
        ),
        Node(
            package='moveit_driver',
            executable='joint_goal',
            output='screen',
            name='joint_goal'
        ),
        Node(
            package='moveit_driver',
            executable='line_goal',
            output='screen',
            name='line_goal'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('ur_robot_driver'),
                    'launch',
                    'ur5e.launch.py'
                ])
            ]),
            launch_arguments={
                'robot_ip': '192.168.56.10',
                'use_fake_hardware': 'false',
                'launch_rviz': 'false',
                'initial_joint_controller': 'joint_trajectory_controller'
            }.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('ur_moveit_config'),
                    'launch',
                    'ur_moveit.launch.py'
                ])
            ]),
            launch_arguments={
                'ur_type': 'ur5e',
                'use_fake_hardware': 'false',
                'launch_rviz': 'true'
            }.items()
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
                'align_depth.enable': 'true',
                'serial_no': "'844212070148'",
                'camera_name': 'Armcamera',
                'rgb_camera.color_profile': '1920x1080x30'
            }.items()
        ),
    ])