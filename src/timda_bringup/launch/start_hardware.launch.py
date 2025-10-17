from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration , PathJoinSubstitution


from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='mecanum',
            executable='mobile_node',
            output='screen',
            name='mobile_node'
        ),
        Node(
            package='linear_move',
            executable='slide',
            output='screen',
            name='slide'
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('timda_bringup'),
                    'launch',
                    'urg_lidar.launch.py'
                ])
            ]),
        ),
        
    ])