import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
from ament_index_python.packages import get_package_share_directory
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():

    moveit_config = (
        MoveItConfigsBuilder(
            robot_name="ur5e", package_name="ur_moveit_config"
        )
        .robot_description(file_path=get_package_share_directory("ur_description") + "/urdf/ur.urdf.xacro",
                           mappings={"name": "ur", "prefix": ""})
        .robot_description_semantic(file_path=get_package_share_directory("ur_moveit_config") + "/srdf/ur.srdf.xacro"
                                    ,mappings={"prefix": "", "name": "ur"})
        .trajectory_execution(file_path=get_package_share_directory("ur_moveit_config") + "/config/controllers.yaml")
        .moveit_cpp(
            file_path=get_package_share_directory("moveit_driver")
            + "/config/moveit_cpp.yaml"
        )
        .to_moveit_configs()
    )

    cpp_node = DeclareLaunchArgument(
        "cpp_node",
        default_value="pose_goal",
        description="C++ API file name",
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="both",
        parameters=[moveit_config.robot_description],
    )
    moveit_cpp_node = Node(
        name="moveit_cpp",
        package="moveit_driver",
        executable=LaunchConfiguration("cpp_node"),
        output="both",
        parameters=[moveit_config.to_dict()],
    )




    return LaunchDescription(
        [
            cpp_node,
            moveit_cpp_node,
            robot_state_publisher,
        ]
    )