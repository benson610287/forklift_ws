FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04
############################## SYSTEM PARAMETERS ##############################
# * Arguments
ARG USER=initial
ARG GROUP=initial
ARG UID=1000
ARG GID="${UID}"
ARG SHELL=/bin/bash
ARG HARDWARE=x86_64
ARG ENTRYPOINT_FILE=entrypint.sh

# * Env vars for the nvidia-container-runtime.
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES all
ENV ROS_DISTRO=humble
# ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

# * Setup users and groups
RUN groupadd --gid "${GID}" "${GROUP}" \
    && useradd --gid "${GID}" --uid "${UID}" -ms "${SHELL}" "${USER}" \
    && mkdir -p /etc/sudoers.d \
    && echo "${USER}:x:${UID}:${UID}:${USER},,,:/home/${USER}:${SHELL}" >> /etc/passwd \
    && echo "${USER}:x:${UID}:" >> /etc/group \
    && echo "${USER} ALL=(ALL) NOPASSWD: ALL" > "/etc/sudoers.d/${USER}" \
    && chmod 0440 "/etc/sudoers.d/${USER}"

# * Replace apt urls
# ? Change to tku
RUN sed -i 's@archive.ubuntu.com@ftp.tku.edu.tw@g' /etc/apt/sources.list
# ? Change to Taiwan
# RUN sed -i 's@archive.ubuntu.com@tw.archive.ubuntu.com@g' /etc/apt/sources.list

# * Time zone
ENV TZ=Asia/Taipei
RUN ln -snf /usr/share/zoneinfo/"${TZ}" /etc/localtime && echo "${TZ}" > /etc/timezone

# * Copy custom configuration
# ? Requires docker version >= 17.09
COPY --chmod=0775 ./${ENTRYPOINT_FILE} /entrypoint.sh
COPY --chown="${USER}":"${GROUP}" --chmod=0775 config config
# ? docker version < 17.09
# COPY ./${ENTRYPOINT_FILE} /entrypoint.sh
# COPY config config
# RUN sudo chmod 0775 /entrypoint.sh && \
    # sudo chown -R "${USER}":"${GROUP}" config \
    # && sudo chmod -R 0775 config

############################### INSTALL #######################################
# * Install packages
RUN apt update \
    && apt install -y --no-install-recommends \
        sudo \
        git \
        htop \
        wget \
        curl \
        psmisc \
        # * Shell
        tmux \
        terminator \
        # * base tools
        udev \
        python3-pip \
        python3-dev \
        python3-setuptools \
        # python3-colcon-common-extensions \
        software-properties-common \
        lsb-release \
        libmodbus-dev \
        # ros-humble-rmw-cyclonedds-cpp \
        # * Work tools
    && apt clean \
    && rm -rf /var/lib/apt/lists/*



# gnome-terminal libcanberra-gtk-module libcanberra-gtk3-module \
# dbus-x11 libglvnd0 libgl1 libglx0 libegl1 libxext6 libx11-6 \
# display dep
# libnss3 libgbm1 libxshmfence1 libdrm2 libx11-xcb1 libxcb-*-dev

ENV DEBIAN_FRONTEND=noninteractive
RUN sudo add-apt-repository universe
RUN sudo apt update
RUN sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key  -o /usr/share/keyrings/ros-archive-keyring.gpg
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN sudo apt update
# RUN sudo  apt install -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" keyboard-configuration
RUN sudo DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop
#ROS2 Cyclone DDS
RUN sudo apt install -y ros-humble-rmw-cyclonedds-cpp
#colcon depend
#colcon depend
RUN apt update \
    && apt install -y python3-colcon-common-extensions\
    	ros-humble-pcl-ros\
	ros-humble-diagnostic-updater\
	ros-humble-laser-proc\
	ros-humble-urg-c\
	ros-humble-urg-node-msgs\
	#ros-humble-xacro\
        ros-humble-urg-node
# 安裝ROS2相關套件
RUN apt-get update && apt-get install -y \
    ros-${ROS_DISTRO}-ur \
    libcap-dev\
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

RUN pip install setuptools==58.2.0
RUN pip install pip==22.0 \
	matplotlib==3.5.1 \
	numpy==1.22.3 \
	pybullet==3.2.5 \
	gym==0.21.0 \
	stable-baselines3==1.7.0 \
	torch==2.0.0 \
	tensorboard==2.12.0 \
	ultralytics \
	numpy==1.22.3 \
	matplotlib==3.5.1 
RUN mkdir -p /etc/apt/keyrings
RUN curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp | sudo tee /etc/apt/keyrings/librealsense.pgp > /dev/null
RUN apt-get install apt-transport-https
RUN echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo `lsb_release -cs` main" | sudo tee /etc/apt/sources.list.d/librealsense.list
RUN apt-get update
RUN apt-get install -y librealsense2-utils
RUN apt-get install -y librealsense2-dev
RUN apt install -y ros-humble-realsense2-camera

#GUI require
RUN pip install pyqt5-tools
RUN sudo apt-get install pyqt5-dev-tools

#GUI require





#RUN sudo apt install -y python3-pip 
#RUN sudo apt install -y python3-dev 
#RUN sudo apt install -y python3-setuptools

RUN ./config/pip/pip_setup.sh

############################## USER CONFIG ####################################
# * Switch user to ${USER}
USER ${USER}

RUN ./config/shell/bash_setup.sh "${USER}" "${GROUP}" \
    && ./config/shell/terminator/terminator_setup.sh "${USER}" "${GROUP}" \
    && ./config/shell/tmux/tmux_setup.sh "${USER}" "${GROUP}" \
    && sudo rm -rf /config
    
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc

# * Switch workspace to ~/work
RUN sudo mkdir -p /home/"${USER}"/work
WORKDIR /home/"${USER}"/work

# * Make SSH available
EXPOSE 22

ENTRYPOINT [ "/entrypoint.sh", "terminator" ]
# ENTRYPOINT [ "/entrypoint.sh", "tmux" ]
# ENTRYPOINT [ "/entrypoint.sh", "bash" ]
# ENTRYPOINT [ "/entrypoint.sh" ]
