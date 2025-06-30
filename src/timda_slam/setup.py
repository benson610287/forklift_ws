from setuptools import find_packages, setup
import glob
import os

package_name = 'timda_slam'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob('launch/*.launch.py')),
        ('share/' + package_name + '/config', glob.glob('config/*.yaml')),
        *([('share/' + package_name + '/maps', glob.glob('maps/*'))] if os.path.isdir('maps') else []),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='flash',
    maintainer_email='flash@todo.todo',
    description='TIMDA機器人SLAM和導航包',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'pose_navigation_node = timda_slam.pose_navigation_node:main',
        ],
    },
)
