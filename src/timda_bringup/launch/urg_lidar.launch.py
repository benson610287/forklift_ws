from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution
from launch_ros.parameter_descriptions import ParameterValue
from typing import List  # 匯入 List
def generate_launch_description():
    robot_description_content = ParameterValue(Command([
        'xacro ',
        PathJoinSubstitution([
            FindPackageShare('forkift_urdf'),
            'urdf',
            'car_ur5_20250118_urdf.urdf'
        ])
    ]),
    value_type=str
    )
    # Robot State Publisher Node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content,
                     'publish_frequency': 30.0}]
    )
     # Urg Node Front
    urg_node_front = Node(
        package='urg_node',
        executable='urg_node_driver',
        name='urg_node_front',
        output='screen',
        parameters=[
            {'laser_frame_id': 'laser_front'},
            {'ip_address': ''},
            {'serial_port': '/dev/ttyACM0'},
            {'serial_baud': 115200},
            {'frame_id': 'laser_front'},
            {'calibrate_time': True},
            {'publish_intensity': False},
            {'publish_multiecho': False},
            {'angle_min': -2.35619449},
            {'angle_max': 2.35619449}
        ],
        remappings=[('/scan', '/scan_front')]
    )

    # Urg Node Back
    urg_node_back = Node(
        package='urg_node',
        executable='urg_node_driver',
        name='urg_node_back',
        output='screen',
        parameters=[
            {'laser_frame_id': 'laser_back'},
            {'ip_address': ''},
            {'serial_port': '/dev/ttyACM1'},
            {'serial_baud': 115200},
            {'frame_id': 'laser_back'},
            {'calibrate_time': True},
            {'publish_intensity': False},
            {'publish_multiecho': False},
            {'angle_min': -2.35619449},
            {'angle_max': 2.35619449}
        ],
        remappings=[('/scan', '/scan_back')]
    )

    # Include laserscan_multi_merger Node
    laserscan_multi_merger = Node(
        package='ira_laser_tools',
        executable='laserscan_multi_merger',
        name='laserscan_multi_merger',
        output='screen',
        parameters=[{
            'destination_frame': 'base_link',
            'cloud_destination_topic': '/merged_cloud',
            'scan_destination_topic': '/scan_multi',
            'laserscan_topics': '/scan_front /scan_back',
            'angle_min': -3.14159265359,
            'angle_max': 3.14159265359,
            'angle_increment': 0.0058,
            'scan_time': 0.0333333,
            'range_min': 0.30,
            'range_max': 50.0,
        }]
    )




    static_tf_map_to_base = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_tf_map_to_base',
    arguments=['0', '0', '0', '0', '0', '0', 'map', 'base_link'],
    output='screen'
    )
    static_tf_map_to_front = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_tf_map_to_front',
    arguments=['0', '0', '0', '3.14', '0', '0', 'base_link', 'laser_front'],
    output='screen'
    )
    static_tf_map_to_back = Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    name='static_tf_map_to_back',
    arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'laser_back'],
    output='screen'
    )










    return LaunchDescription([
        robot_state_publisher_node,
        urg_node_front,
        urg_node_back,
        laserscan_multi_merger,
        static_tf_map_to_base,
        static_tf_map_to_front,
        static_tf_map_to_back
    ])


# <launch>

# <!-- A simple launch file for the urg_node package. -->
# <arg name="model" default="$(find-pkg-share timda_sim)/mobile_description/urdf/timda_mobile_platform.urdf"/>
# <!--  When using an IP-connected LIDAR, populate the "ip_address" parameter with the address of the LIDAR.
#       Otherwise, leave it blank. If supported by your LIDAR, you may enable the publish_intensity
#       and/or publish_multiecho options. -->
#   <node name="robot_state_publisher" pkg="robot_state_publisher" exec="robot_state_publisher" output="screen">
#     <!-- <param name="robot_description" value="$(find-pkg-share mobile_description)/urdf/timda_mobile_platform.urdf"/> -->
#     <param name="robot_description" command="xacro  $(arg model)" />
#     <param name="publish_frequency" value="30.0" />
#   </node>
#   <!-- <node name="robot_state_publisher" pkg="robot_state_publisher" exec="robot_state_publisher" output="screen">
#     <param name="robot_description" value="$(find-pkg-share mobile_description)/urdf/timda_mobile_platform.urdf" />
#     <param name="publish_frequency" value="30.0" /> -->
#   <!-- </node> -->

#   <!-- <node name="urg_node_front" pkg="urg_node" exec="urg_node_driver" output="screen">
#     <param name="laser_frame_id" value="front_lidar_frame"/>
#     <param name="ip_address" value=""/>
#     <param name="serial_port" value="/dev/ttyACM0"/>
#     <param name="serial_baud" value="115200"/> -->
#     <!-- <param name="frame_id" value="laser_front"/> -->
#     <!-- <param name="calibrate_time" value="false"/>
#     <param name="publish_intensity" value="false"/>
#     <param name="publish_multiecho" value="false"/>
#     <param name="angle_min" value="-2.35619449"/>
#     <param name="angle_max" value="2.35619449"/>
#     <remap from="/scan" to="/scan_front" />
#   </node> -->
#   <!-- <node name="urg_node_back" pkg="urg_node" exec="urg_node_driver" output="screen">
#     <param name="laser_frame_id" value="back_lidar_frame"/>
#     <param name="ip_address" value=""/>
#     <param name="serial_port" value="/dev/ttyACM1"/>
#     <param name="serial_baud" value="115200"/> -->
#     <!-- <param name="frame_id" value="laser_back"/> -->
#     <!-- <param name="calibrate_time" value="false"/>
#     <param name="publish_intensity" value="false"/>
#     <param name="publish_multiecho" value="false"/>
#     <param name="angle_min" value="-2.35619449"/>
#     <param name="angle_max" value="2.35619449"/>
#     <remap from="/scan" to="/scan_back" />
#   </node> -->
#   <!-- <include file="$(find-pkg-share ira_laser_tools)/launch/laserscan_multi_merger.launch" /> -->



# </launch>
