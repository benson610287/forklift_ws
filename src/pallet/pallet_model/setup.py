from setuptools import find_packages, setup

package_name = 'pallet_model'
submodules="pallet_model/Pallet_RL"
setup(
    name=package_name,
    version='0.0.0',
    # packages=find_packages(exclude=['test']),
    # packages=[package_name,submodules],
    packages=find_packages(include=['pallet_model', 'pallet_model.*']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools','gym'],
    zip_safe=True,
    maintainer='aa',
    maintainer_email='aa@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "main=pallet_model.main:main",
            "single_main=pallet_model.single_main:main"
        ],
    },
)
