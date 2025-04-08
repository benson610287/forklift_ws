from setuptools import find_packages, setup

package_name = 'pallet_main'

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
    maintainer='aa',
    maintainer_email='aa@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        'handcamera=pallet_main.handcamera:main',
        'GetBox=pallet_main.GetBox:main',
        'PalletMain=pallet_main.PalletMain:main'
        ],
    },
)
