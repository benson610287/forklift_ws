FROM ubuntu:22.04

############################## SYSTEM PARAMETERS ##############################
ARG USER=initial
ARG GROUP=initial
ARG UID=1000
ARG GID="${UID}"
ARG SHELL=/bin/bash
ARG HARDWARE=x86_64
ARG ENTRYPOINT_FILE=entrypint.sh

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV ROS_DISTRO=humble
# ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

# Setup user and group
RUN groupadd --gid "${GID}" "${GROUP}" && \
    useradd --gid "${GID}" --uid "${UID}" -ms "${SHELL}" "${USER}" && \
    mkdir -p /etc/sudoers.d && \
    echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" && \
    chmod 0440 "/etc/sudoers.d/${USER}"

# Change APT mirror to Taiwan
RUN sed -i 's@archive.ubuntu.com@tw.archive.ubuntu.com@g' /etc/apt/sources.list

# Timezone
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/"${TZ}" /etc/localtime && echo "${TZ}" > /etc/timezone

# Copy configuration files
COPY --chmod=0775 ./${ENTRYPOINT_FILE} /entrypoint.sh
COPY --chown="${USER}":"${GROUP}" --chmod=0775 config config

############################### INSTALL BASE ##################################
RUN apt update && apt install -y --no-install-recommends \
    sudo git htop wget curl psmisc \
    tmux terminator udev \
    python3-pip python3-dev python3-setuptools \
    software-properties-common lsb-release libmodbus-dev && \
    apt clean && rm -rf /var/lib/apt/lists/*

# ROS 2 sources & key
RUN add-apt-repository universe && \
    curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    > /etc/apt/sources.list.d/ros2.list && \
    apt update && apt upgrade -y && apt --fix-broken install -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop ros-humble-rmw-cyclonedds-cpp

# ROS packages and colcon tools
RUN apt update && apt install -y \
    python3-colcon-common-extensions \
    ros-humble-pcl-ros \
    ros-humble-diagnostic-updater \
    ros-humble-laser-proc \
    ros-humble-urg-c \
    ros-humble-urg-node-msgs \
    ros-humble-xacro \
    ros-humble-cv-bridge \
    ros-humble-librealsense2*

############################## REALSENSE & LIBS ###############################
# Add RealSense source & install librealsense2
RUN mkdir -p /etc/apt/keyrings && \
    curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp | tee /etc/apt/keyrings/librealsense.pgp > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/librealsense.list && \
    apt update && apt install -y librealsense2-dev librealsense2-utils

ENV DEBIAN_FRONTEND=noninteractive
RUN sudo add-apt-repository universe
RUN sudo apt update
RUN sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN sudo apt update && sudo apt upgrade -y && sudo apt --fix-broken install -y
# RUN sudo  apt install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" keyboard-configuration
RUN sudo DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop
#ROS2 Cyclone DDS
RUN sudo apt install -y ros-humble-rmw-cyclonedds-cpp
#colcon depend
RUN apt update \
    && apt install -y python3-colcon-common-extensions \
	ros-humble-pcl-ros\
	ros-humble-diagnostic-updater\
	ros-humble-laser-proc\
	ros-humble-urg-c\
	ros-humble-urg-node-msgs\
	#ros-humble-xacro\
        ros-humble-urg-node
        #ros-humble-ur

# 安裝ROS2相關套件
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ur \
    ros-${ROS_DISTRO}-rosidl-default-generators \
    ros-${ROS_DISTRO}-action-msgs \
    ros-${ROS_DISTRO}-ur-msgs \
    ros-${ROS_DISTRO}-controller-interface \
    ros-${ROS_DISTRO}-joint-trajectory-controller \
    ros-${ROS_DISTRO}-controller-manager \
    ros-${ROS_DISTRO}-moveit-simple-controller-manager \
    ros-${ROS_DISTRO}-ament-cmake \
    ros-${ROS_DISTRO}-xacro \
    ros-${ROS_DISTRO}-test-msgs \
    ros-${ROS_DISTRO}-ackermann-msgs \
    python3-ament-package \
    && rm -rf /var/lib/apt/lists/*
	#ros-humble-urg-node





RUN pip install setuptools==58.2.0
#GUI require
RUN pip install pyqt5-tools \ 
	opencv-python-headless
RUN apt-get update && apt-get install -y \
	qttools5-dev-tools


	
############################## PYTHON LIBS ####################################
RUN pip install setuptools==58.2.0 && \
    pip install pyrealsense2 ultralytics open3d && \
    pip install 'numpy<2.0' --force-reinstall && \
    pip install opencv-python

RUN apt install -y pyqt5-dev-tools

############################## USER CONFIG ####################################
#GUI require

#RUN sudo apt install -y python3-pip 
#RUN sudo apt install -y python3-dev 
#RUN sudo apt install -y python3-setuptools
RUN apt update


##################### ZACK ADD BEGIN ##################################
###################### RealSense #############################
RUN mkdir -p /etc/apt/keyrings
RUN curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null
RUN echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo `lsb_release -cs` main" \
    | tee /etc/apt/sources.list.d/librealsense.list


RUN apt update && apt install -y \
    # ros2 
    python3-rosdep \
    # realsense
    librealsense2-utils \
    librealsense2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install setuptools \
    pyrealsense2
    # opencv-contrib-python==4.11.0.86

RUN ./config/pip/pip_setup.sh
##################### ZACK ADD END ##################################

############################## USER CONFIG ####################################
#* Switch user to ${USER}

USER ${USER}
RUN ./config/shell/bash_setup.sh "${USER}" "${GROUP}" && \
    ./config/shell/terminator/terminator_setup.sh "${USER}" "${GROUP}" && \
    ./config/shell/tmux/tmux_setup.sh "${USER}" "${GROUP}" && \
    sudo rm -rf /config

RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc

# Workspace & default workdir
RUN sudo mkdir -p /home/"${USER}"/work
WORKDIR /home/"${USER}"/work

# SSH port
EXPOSE 22

ENTRYPOINT [ "/entrypoint.sh", "terminator" ]

