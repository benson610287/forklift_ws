from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration , PathJoinSubstitution


from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    return LaunchDescription([
        
        Node(
            package='main_control',
            executable='main',
            output='screen',
            name='main'
        ),
        Node(
            package='main_control',
            executable='fake_auto',
            output='screen',
            name='fake_auto'
        ),

    ])