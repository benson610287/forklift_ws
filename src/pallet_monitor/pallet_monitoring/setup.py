from setuptools import find_packages, setup

package_name = 'pallet_monitoring'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/img', ['img/test_image.jpg']),
        ('share/' + package_name + '/launch', ['launch/pallet_monitoring.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='iclab',
    maintainer_email='wengkunduo@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'yolo = pallet_monitoring.pallet_yolo_detector:main',
            'cropper = pallet_monitoring.pallet_cropper:main',
            'clutter = pallet_monitoring.pallet_clutter_evaluator:main',
            'decision = pallet_monitoring.pallet_decision:main',
            'pub = pallet_monitoring.img_pub:main',
        ],
    },
)
