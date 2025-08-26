import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Pose, PoseArray, Twist
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import Int64
from interface.srv import Maincontroller
from cv_bridge import CvBridge
import os
import configparser

import numpy as np
from scipy.spatial.transform import Rotation as R
import time
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import threading
from collections import deque


class PlotOrientationNode(Node):
    def __init__(self):
        super().__init__('plot_orientation_node')
        self.shelf_pose_subscriber = self.create_subscription(PoseArray, 'aruco_detect', self.pose_callback, 10)
        self.service = self.create_service(Maincontroller, 'shelf_docking', self.service_callback)
        self.linear_motor_publisher = self.create_publisher(Int64, 'topic', 10)
        self.mecanum_publisher = self.create_publisher(Twist, 'cmd_vel', 10)
        
        # Data storage for plotting
        self.max_points = 100  # Maximum points to keep in plot
        self.time_data = deque(maxlen=self.max_points)
        self.rx_data = deque(maxlen=self.max_points)
        self.ry_data = deque(maxlen=self.max_points)
        self.rz_data = deque(maxlen=self.max_points)
        
        # Initialize plotting
        self.start_time = time.time()
        self.plot_counter = 0
        self.last_plot_time = 0
        self.plot_interval = 2.0  # Update plot every 2 seconds
        
        # Create output directory
        self.output_dir = '/tmp/orientation_plots'
        os.makedirs(self.output_dir, exist_ok=True)
        
    def pose_callback(self, msg):
        current_time = time.time() - self.start_time
        
        for i, pose in enumerate(msg.poses):
            # Check if pose has valid data (non-zero quaternion)
            quat = [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]
            if any(abs(q) > 1e-6 for q in quat):  # Check if quaternion is not all zeros
                
                # Convert quaternion to Euler angles
                r = R.from_quat(quat)
                euler_angles = r.as_euler('xyz', degrees=True)  # Roll, Pitch, Yaw in degrees
                
                rx, ry, rz = euler_angles
                
                # Print pose information
                self.get_logger().info(f'Marker {i} - Position: x={pose.position.x:.3f}, y={pose.position.y:.3f}, z={pose.position.z:.3f}')
                self.get_logger().info(f'Marker {i} - Orientation (Euler): rx={rx:.2f}°, ry={ry:.2f}°, rz={rz:.2f}°')
                
                # Store data for plotting (only for first valid marker for simplicity)
                if i == 0:  # Plot data for marker 0
                    self.time_data.append(current_time)
                    self.rx_data.append(rx)
                    self.ry_data.append(ry)
                    self.rz_data.append(rz)
                    
                    # Update plot periodically
                    if current_time - self.last_plot_time > self.plot_interval:
                        self.update_plot()
                        self.last_plot_time = current_time
                
                break  # Only process first valid pose for now
    
    def update_plot(self):
        """Update and save the plot"""
        if len(self.time_data) > 5:  # Only plot if we have enough data points
            try:
                plt.figure(figsize=(12, 8))
                
                # Plot each orientation component
                plt.subplot(3, 1, 1)
                plt.plot(list(self.time_data), list(self.rx_data), 'r-', linewidth=2, label='Roll (rx)')
                plt.ylabel('Roll (degrees)')
                plt.grid(True)
                plt.legend()
                plt.title('ArUco Marker Orientation (Euler Angles)')
                
                plt.subplot(3, 1, 2)
                plt.plot(list(self.time_data), list(self.ry_data), 'g-', linewidth=2, label='Pitch (ry)')
                plt.ylabel('Pitch (degrees)')
                plt.grid(True)
                plt.legend()
                
                plt.subplot(3, 1, 3)
                plt.plot(list(self.time_data), list(self.rz_data), 'b-', linewidth=2, label='Yaw (rz)')
                plt.ylabel('Yaw (degrees)')
                plt.xlabel('Time (s)')
                plt.grid(True)
                plt.legend()
                
                plt.tight_layout()
                
                # Save plot
                self.plot_counter += 1
                filename = f'{self.output_dir}/orientation_plot_{self.plot_counter:04d}.png'
                plt.savefig(filename, dpi=150, bbox_inches='tight')
                plt.close()
                
                self.get_logger().info(f'Plot saved to: {filename}')
                
                # Also create a combined plot
                plt.figure(figsize=(10, 6))
                plt.plot(list(self.time_data), list(self.rx_data), 'r-', linewidth=2, label='Roll (rx)')
                plt.plot(list(self.time_data), list(self.ry_data), 'g-', linewidth=2, label='Pitch (ry)')
                plt.plot(list(self.time_data), list(self.rz_data), 'b-', linewidth=2, label='Yaw (rz)')
                
                plt.title('ArUco Marker Orientation (Euler Angles)')
                plt.xlabel('Time (s)')
                plt.ylabel('Angle (degrees)')
                plt.grid(True)
                plt.legend()
                plt.ylim(-180, 180)
                
                # Save combined plot
                combined_filename = f'{self.output_dir}/orientation_combined_{self.plot_counter:04d}.png'
                plt.savefig(combined_filename, dpi=150, bbox_inches='tight')
                plt.close()
                
                # Keep only the latest plot (overwrite)
                latest_filename = f'{self.output_dir}/orientation_latest.png'
                plt.figure(figsize=(10, 6))
                plt.plot(list(self.time_data), list(self.rx_data), 'r-', linewidth=2, label='Roll (rx)')
                plt.plot(list(self.time_data), list(self.ry_data), 'g-', linewidth=2, label='Pitch (ry)')
                plt.plot(list(self.time_data), list(self.rz_data), 'b-', linewidth=2, label='Yaw (rz)')
                
                plt.title('ArUco Marker Orientation (Euler Angles) - Latest')
                plt.xlabel('Time (s)')
                plt.ylabel('Angle (degrees)')
                plt.grid(True)
                plt.legend()
                plt.ylim(-180, 180)
                
                plt.savefig(latest_filename, dpi=150, bbox_inches='tight')
                plt.close()
                
            except Exception as e:
                self.get_logger().error(f"Plot update error: {e}")
    
    def service_callback(self, request, response):
        # Your service implementation here
        self.get_logger().info(f'Service called with: {request}')
        return response

def main():
    rclpy.init()
    node = PlotOrientationNode()

    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        node.get_logger().info(f'Plot output directory: {node.output_dir}')
        node.get_logger().info('Monitor orientation plots in /tmp/orientation_plots/')
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
