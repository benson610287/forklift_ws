from setuptools import find_packages, setup
import os
from glob import glob
package_name = 'docking_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        ('share/docking_pkg/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eating',
    maintainer_email='eating@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'docking_status_server = docking_pkg.docking_status_server:main',
            'dockingcamera = docking_pkg.dockingcamera:main',
            'yolo_subscriber = docking_pkg.yolo_subscriber:main',
            'YoloDepthProcessor = docking_pkg.YoloDepthProcessor:main',
            'ransac = docking_pkg.ransac:main',
            'pid_mecanum_node = docking_pkg.pid_mecanum_node:main',
            'docking_processor_node = docking_pkg.docking_processor_node:main',

        ],
    },
)
