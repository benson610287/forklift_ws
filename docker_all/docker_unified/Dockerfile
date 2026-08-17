# Unified image for the whole forklift stack:
# ros2 (base/UR/GUI) + hyslam (nav2/slam) + pallet (YOLO/RL) + shelf (aruco/Azure) + docking
# Replaces docker_ros2 / docker_hyslam / docker_pallet / docker_shelf / docker_docking.
# NOTE: host needs NVIDIA driver >= 550 for CUDA 12.8 images (check with nvidia-smi).
FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04
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
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=all
ENV ROS_DISTRO=humble

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
COPY --chmod=0775 ./${ENTRYPOINT_FILE} /entrypoint.sh
COPY --chown="${USER}":"${GROUP}" --chmod=0775 config config

############################### INSTALL #######################################
# * Base tools
RUN apt update \
    && apt install -y --no-install-recommends \
    sudo \
    git \
    htop \
    nvtop \
    wget \
    curl \
    psmisc \
    openssh-server \
    usbutils \
    apt-transport-https \
    # * Shell
    tmux \
    terminator \
    # * base tools
    udev \
    python3-pip \
    python3-dev \
    python3-setuptools \
    software-properties-common \
    lsb-release \
    gnupg \
    libmodbus-dev \
    libcap-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

ENV DEBIAN_FRONTEND=noninteractive

# * ROS 2 Humble
RUN sudo add-apt-repository universe
# ROS signing key rotated in 2025 — use the official ros2-apt-source package instead of a raw key fetch
RUN ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F '"tag_name"' | awk -F'"' '{print $4}') \
    && curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${VERSION_CODENAME})_all.deb" \
    && apt update && apt install -y /tmp/ros2-apt-source.deb \
    && rm /tmp/ros2-apt-source.deb
RUN sudo apt update && sudo DEBIAN_FRONTEND=noninteractive apt install -y ros-humble-desktop
RUN sudo apt install -y ros-humble-rmw-cyclonedds-cpp python3-colcon-common-extensions python3-rosdep

# * ROS 2 package union (base drivers / lidar / UR arm + MoveIt / Nav2 + SLAM / cameras)
RUN apt update && apt install -y \
    # lidar + pointcloud
    ros-humble-pcl-ros \
    ros-humble-diagnostic-updater \
    ros-humble-laser-proc \
    ros-humble-urg-c \
    ros-humble-urg-node-msgs \
    ros-humble-urg-node \
    # UR arm + MoveIt + ros2_control
    ros-humble-ur \
    ros-humble-ur-msgs \
    ros-humble-controller-interface \
    ros-humble-joint-trajectory-controller \
    ros-humble-controller-manager \
    ros-humble-moveit-simple-controller-manager \
    # nav2 + slam (from docker_hyslam)
    ros-humble-navigation2 \
    ros-humble-nav2-bringup \
    ros-humble-slam-toolbox \
    # misc build/msg deps
    ros-humble-rosidl-default-generators \
    ros-humble-action-msgs \
    ros-humble-ament-cmake \
    ros-humble-xacro \
    ros-humble-cv-bridge \
    ros-humble-test-msgs \
    ros-humble-ackermann-msgs \
    python3-ament-package \
    && rm -rf /var/lib/apt/lists/*

###################### RealSense #############################
# fetch keys + install in ONE layer so the signing keys are never a stale cached layer.
# The repo moved to a new signing key (RealSense spin-out, Nov 2025, FB0B24895113F120)
# but the .pgp URL still serves the old 2018 key — install both.
RUN mkdir -p /etc/apt/keyrings \
    && curl -sSf https://librealsense.intel.com/Debian/librealsense.pgp -o /etc/apt/keyrings/librealsense.pgp \
    && curl -sSf "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xFB0B24895113F120" \
    | gpg --dearmor >> /etc/apt/keyrings/librealsense.pgp \
    && echo "deb [signed-by=/etc/apt/keyrings/librealsense.pgp] https://librealsense.intel.com/Debian/apt-repo `lsb_release -cs` main" \
    | tee /etc/apt/sources.list.d/librealsense.list \
    && apt update && apt install -y \
    librealsense2-utils \
    librealsense2-dev \
    ros-humble-realsense2-camera \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#################### Kinect Azure (from docker_shelf) ###############################
RUN apt-get update && apt install -y \
    libgl1-mesa-dev libsoundio-dev libvulkan-dev libx11-dev libxcursor-dev libxinerama-dev libxrandr-dev libusb-1.0-0-dev libssl-dev libudev-dev mesa-common-dev uuid-dev

WORKDIR /home/${USER}/work/azure
RUN wget https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/k/k4a-tools/k4a-tools_1.4.2_amd64.deb
RUN wget https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4-dev/libk4a1.4-dev_1.4.2_amd64.deb
RUN wget https://packages.microsoft.com/ubuntu/18.04/prod/pool/main/libk/libk4a1.4/libk4a1.4_1.4.2_amd64.deb
RUN wget http://ftp.de.debian.org/debian/pool/main/libs/libsoundio/libsoundio1_1.1.0-1_amd64.deb
RUN ACCEPT_EULA=Y dpkg -i libk4a1.4_1.4.2_amd64.deb && \
    dpkg -i libk4a1.4-dev_1.4.2_amd64.deb
RUN dpkg -i libsoundio1_1.1.0-1_amd64.deb
RUN dpkg -i k4a-tools_1.4.2_amd64.deb
RUN rm libk4a1.4_1.4.2_amd64.deb \
    libk4a1.4-dev_1.4.2_amd64.deb \
    libsoundio1_1.1.0-1_amd64.deb \
    k4a-tools_1.4.2_amd64.deb
WORKDIR /home/${USER}/work/azure
RUN git clone https://github.com/microsoft/Azure-Kinect-Sensor-SDK.git
WORKDIR /home/${USER}/work/azure/Azure-Kinect-Sensor-SDK
RUN mkdir -p /etc/udev/rules.d/ && \
    cp ./scripts/99-k4a.rules /etc/udev/rules.d/
RUN rm -rf /home/${USER}/work/azure/Azure-Kinect-Sensor-SDK
WORKDIR /

#################### GUI (from docker_ros2) ######################
RUN apt-get update && apt-get install -y qttools5-dev-tools pyqt5-dev-tools
RUN pip install setuptools==58.2.0 pyqt5-tools

#################### RL stack for pallet_model (from docker_pallet) ######################
# gym==0.21.0 (required by stable-baselines3 1.7.0) only installs with pip 22 + setuptools 58
RUN pip install pip==22.0 && \
    pip install --ignore-installed \
    pybullet==3.2.5 \
    gym==0.21.0 \
    stable-baselines3==1.7.0 \
    tensorboard==2.12.0 \
    matplotlib==3.5.1

#################### Common pip deps (config/pip/requirements.txt) ######################
RUN ./config/pip/pip_setup.sh

#################### PyTorch cu128 (installed LAST so it wins over RL layer's torch) ####
RUN pip3 install --ignore-installed torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
# clean up matplotlib mixed-version install (3.5.1 pin overwritten by ultralytics' newer pull)
RUN pip3 uninstall -y matplotlib || true
RUN rm -rf /usr/local/lib/python3.10/dist-packages/matplotlib* \
    && pip3 install matplotlib \
    && python3 -c "import matplotlib.pyplot"

############################## USER CONFIG ####################################
#* Switch user to ${USER}
USER ${USER}

RUN ./config/shell/bash_setup.sh "${USER}" "${GROUP}" \
    && ./config/shell/terminator/terminator_setup.sh "${USER}" "${GROUP}" \
    && ./config/shell/tmux/tmux_setup.sh "${USER}" "${GROUP}" \
    && sudo rm -rf /config

ARG ROS_DOMAIN_ID=42
RUN echo "export ROS_DOMAIN_ID=$ROS_DOMAIN_ID" >> ~/.bashrc
RUN echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> ~/.bashrc
# NIC pin is machine-specific: uncomment and set your wifi/eth interface if multicast leaks across NICs
# RUN echo "export CYCLONEDDS_URI=\"<CycloneDDS><Domain><General><NetworkInterfaceAddress>wlp0s20f3</NetworkInterfaceAddress></General></Domain></CycloneDDS>\"" >> ~/.bashrc
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# * Switch workspace to ~/work
RUN sudo mkdir -p /home/"${USER}"/work
WORKDIR /home/"${USER}"/work

# * Make SSH available
EXPOSE 22

ENTRYPOINT [ "/entrypoint.sh", "terminator" ]
# ENTRYPOINT [ "/entrypoint.sh", "tmux" ]
# ENTRYPOINT [ "/entrypoint.sh", "bash" ]
# ENTRYPOINT [ "/entrypoint.sh" ]
