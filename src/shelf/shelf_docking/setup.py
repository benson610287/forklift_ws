from setuptools import find_packages, setup

package_name = 'shelf_docking'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='flash',
    maintainer_email='flash@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'shelf_docking = shelf_docking.main:main',
            'callback_control = shelf_docking.callback_control:main',
            'plot_live_orientation = shelf_docking.plot_live_oriention:main',
        ],
    },
)
