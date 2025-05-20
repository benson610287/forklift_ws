from setuptools import find_packages
from setuptools import setup

setup(
    name='gui_interface',
    version='0.0.0',
    packages=find_packages(
        include=('gui_interface', 'gui_interface.*')),
)
