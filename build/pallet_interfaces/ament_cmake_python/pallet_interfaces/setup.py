from setuptools import find_packages
from setuptools import setup

setup(
    name='pallet_interfaces',
    version='0.0.0',
    packages=find_packages(
        include=('pallet_interfaces', 'pallet_interfaces.*')),
)
