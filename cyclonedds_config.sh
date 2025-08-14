#!/bin/bash

# ROS2 CycloneDDS WiFi Interface Setup Script
# This script configures ROS2 to use CycloneDDS with a specific WiFi interface

# Configuration variables
ROS_DOMAIN_ID=42
WIFI_INTERFACE="wlp0s20f3"  # Change this to your WiFi interface name

# Set ROS2 environment variables
export ROS_DOMAIN_ID=$ROS_DOMAIN_ID
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export CYCLONEDDS_URI="<CycloneDDS><Domain><General><NetworkInterfaceAddress>$WIFI_INTERFACE</NetworkInterfaceAddress></General></Domain></CycloneDDS>"

# Print current configuration
echo "ROS2 CycloneDDS Configuration:"
echo "  Domain ID: $ROS_DOMAIN_ID"
echo "  RMW Implementation: $RMW_IMPLEMENTATION"
echo "  WiFi Interface: $WIFI_INTERFACE"
echo "  CycloneDDS URI: $CYCLONEDDS_URI"
echo ""
echo "Environment variables set successfully!"
echo ""
echo "To make these permanent, add the export commands to your ~/.bashrc"
echo "To test: ros2 topic list"
