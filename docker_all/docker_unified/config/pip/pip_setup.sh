#!/usr/bin/env bash

# python3 -m pip install --upgrade --force-reinstall pip \
# && pip3 install -r ./pip/requirements.txt
file_dir=$(dirname "$(readlink -f "${0}")")

# --ignore-installed: apt/distutils packages (blinker, sympy, ...) cannot be uninstalled by pip
pip install --upgrade --force-reinstall pip \
&& pip install --ignore-installed -r "${file_dir}"/requirements.txt
