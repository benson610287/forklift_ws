from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    return LaunchDescription([
        # DeclareLaunchArgument('mode',       default_value='train'),
        # DeclareLaunchArgument('box_model',  default_value='1'),
        # DeclareLaunchArgument('bin_model',  default_value='1'),
        # DeclareLaunchArgument('load_model', default_value='12_9'),
        # DeclareLaunchArgument('save_model', default_value='PPO'),
        # DeclareLaunchArgument('train_step', default_value='100000'),
        # DeclareLaunchArgument('episode',    default_value='100'),
        Node(
            package='pallet_main',
            executable='get_box_from_yolo',
            output='screen',
            name='get_box'
        ),
        Node(
            package='pallet_model',
            executable='main',
            # name='multi_pallet_model',
            output='screen',
            arguments=[
                '--mode', 'train',
                '--box_model', '1',
                '--bin_model', '1',
                '--load_model', '12_9',
                '--save_model', 'PPO',
                '--train_step', '100000',
                '--episode', '100',
            ]
        ),
        Node(
            package='pallet_model',
            executable='single_main',
            output='screen',
            name='single_main',
        )
    ])