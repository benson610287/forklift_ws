from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument , IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration , PathJoinSubstitution


from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
    OrSubstitution,
)

def generate_launch_description():
    rviz_config_file = PathJoinSubstitution(
            [FindPackageShare("timda_slam"), "rviz.rviz"]
        )
    return LaunchDescription([

        Node(
            package='timda_slam',
            executable='pose_navigation_node',
            output='screen',
            name='pose_navigation_node'
        ),
        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('timda_slam'),
                    'launch',
                    'navigation.launch.py'
                ])
            ]),
            launch_arguments={
                'pose_navigation': 'False',
            }.items()
        ),
        
        Node(
        package="rviz2",
        # condition=IfCondition(launch_rviz),
        executable="rviz2",
        name="rviz2_slam",
        output="log",
        arguments=["-d", rviz_config_file],
        # parameters=[
        #     robot_description,
        #     robot_description_semantic,
        #     ompl_planning_pipeline_config,
        #     robot_description_kinematics,
        #     robot_description_planning,
        #     warehouse_ros_config,
        #     {
        #         "use_sim_time": use_sim_time,
        #     },
        # ],
        )
    ])