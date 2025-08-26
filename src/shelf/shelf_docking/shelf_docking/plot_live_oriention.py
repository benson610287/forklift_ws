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
matplotlib.use('TkAgg')  # Use interactive backend for live plotting
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
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
        
        # Threading for live plotting
        self.data_lock = threading.Lock()
        self.plot_thread = None
        self.plot_running = True
        
        # Initialize plotting
        self.start_time = time.time()
        self.plot_counter = 0
        self.last_plot_time = 0
        self.plot_interval = 1.0  # Update plot every 1 second (reduced from 2)
        
        # Create output directory in package folder
        package_dir = os.getcwd()
        self.output_dir = os.path.join(package_dir, 'orientation_plots')
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Clean up old plots from /tmp if they exist
        self.cleanup_tmp_plots()
        
        # Start live plotting in separate thread
        self.start_live_plot()
        
    def start_live_plot(self):
        """Start live plotting in a separate thread"""
        self.plot_thread = threading.Thread(target=self.live_plot_worker, daemon=True)
        self.plot_thread.start()
        self.get_logger().info('Live plotting thread started')
        
    def live_plot_worker(self):
        """Worker function for live plotting"""
        try:
            # Setup the plot
            plt.ion()  # Turn on interactive mode
            self.fig, self.ax = plt.subplots(figsize=(12, 8))
            self.ax.set_title('ArUco Marker 3 Orientation (Euler Angles) - Live Plot')
            self.ax.set_xlabel('Time (s)')
            self.ax.set_ylabel('Angle (degrees)')
            self.ax.grid(True)
            self.ax.set_ylim(-180, 180)
            
            # Initialize empty lines
            self.line_rx, = self.ax.plot([], [], 'r-', linewidth=2, label='Roll (rx)', marker='o', markersize=4)
            self.line_ry, = self.ax.plot([], [], 'g-', linewidth=2, label='Pitch (ry)', marker='s', markersize=4)
            self.line_rz, = self.ax.plot([], [], 'b-', linewidth=2, label='Yaw (rz)', marker='^', markersize=4)
            
            self.ax.legend()
            plt.show()
            
            # Main plotting loop
            while self.plot_running:
                try:
                    with self.data_lock:
                        if len(self.time_data) > 0:
                            # Update line data
                            self.line_rx.set_data(list(self.time_data), list(self.rx_data))
                            self.line_ry.set_data(list(self.time_data), list(self.ry_data))
                            self.line_rz.set_data(list(self.time_data), list(self.rz_data))
                            
                            # Update axes limits
                            if len(self.time_data) > 1:
                                self.ax.set_xlim(min(self.time_data) - 1, max(self.time_data) + 1)
                    
                    # Redraw the plot
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
                    
                    time.sleep(0.1)  # Update every 100ms
                    
                except Exception as e:
                    self.get_logger().error(f"Live plot update error: {e}")
                    time.sleep(1.0)  # Wait longer if there's an error
                    
        except Exception as e:
            self.get_logger().error(f"Live plot worker failed: {e}")
        finally:
            if hasattr(self, 'fig'):
                plt.close(self.fig)
        
    def cleanup_tmp_plots(self):
        """Clean up old plots from /tmp directory"""
        try:
            tmp_plot_dir = '/tmp/orientation_plots'
            if os.path.exists(tmp_plot_dir):
                import shutil
                shutil.rmtree(tmp_plot_dir)
                self.get_logger().info(f'Cleaned up old plots from {tmp_plot_dir}')
        except Exception as e:
            self.get_logger().warn(f'Failed to cleanup tmp plots: {e}')
        
    def create_test_plot(self):
        """Create a test plot to verify matplotlib is working"""
        try:
            plt.figure(figsize=(8, 6))
            x = [1, 2, 3, 4, 5]
            y = [10, 20, 15, 25, 30]
            plt.plot(x, y, 'r-', linewidth=2, marker='o', label='Test Data')
            plt.title('Test Plot - Matplotlib Working')
            plt.xlabel('Time')
            plt.ylabel('Value')
            plt.grid(True)
            plt.legend()
            
            test_filename = f'{self.output_dir}/test_plot.png'
            plt.savefig(test_filename, dpi=150, bbox_inches='tight')
            plt.close()
            
            self.get_logger().info(f'Test plot created successfully: {test_filename}')
            
        except Exception as e:
            self.get_logger().error(f"Test plot creation failed: {e}")
        
    def save_plot_to_file(self):
        """Save current plot data to file"""
        if len(self.time_data) > 2:
            try:
                # Create a separate figure for saving
                fig_save, ax_save = plt.subplots(figsize=(10, 6))
                
                with self.data_lock:
                    time_list = list(self.time_data)
                    rx_list = list(self.rx_data)
                    ry_list = list(self.ry_data)
                    rz_list = list(self.rz_data)
                
                ax_save.plot(time_list, rx_list, 'r-', linewidth=2, label='Roll (rx)', marker='o')
                ax_save.plot(time_list, ry_list, 'g-', linewidth=2, label='Pitch (ry)', marker='s')
                ax_save.plot(time_list, rz_list, 'b-', linewidth=2, label='Yaw (rz)', marker='^')
                
                ax_save.set_title('ArUco Marker 3 Orientation (Euler Angles)')
                ax_save.set_xlabel('Time (s)')
                ax_save.set_ylabel('Angle (degrees)')
                ax_save.grid(True)
                ax_save.legend()
                ax_save.set_ylim(-180, 180)
                
                # Save plot
                self.plot_counter += 1
                filename = f'{self.output_dir}/marker3_orientation_{self.plot_counter:04d}.png'
                fig_save.savefig(filename, dpi=150, bbox_inches='tight')
                
                # Save latest plot
                latest_filename = f'{self.output_dir}/marker3_orientation_latest.png'
                fig_save.savefig(latest_filename, dpi=150, bbox_inches='tight')
                
                plt.close(fig_save)
                
                self.get_logger().info(f'Plot saved to: {filename}')
                
            except Exception as e:
                self.get_logger().error(f"Save plot error: {e}")
    
    def destroy_node(self):
        """Clean shutdown"""
        self.plot_running = False
        if self.plot_thread and self.plot_thread.is_alive():
            self.plot_thread.join(timeout=2.0)
        super().destroy_node()

    def pose_callback(self, msg):
        current_time = time.time() - self.start_time
        
        # Look specifically for marker 3
        marker_3_found = False
        
        for i, pose in enumerate(msg.poses):
            # Check if pose has valid data (non-zero quaternion)
            quat = [pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w]
            if any(abs(q) > 1e-6 for q in quat):  # Check if quaternion is not all zeros
                
                # Convert quaternion to Euler angles
                r = R.from_quat(quat)
                euler_angles = r.as_euler('xyz', degrees=True)  # Roll, Pitch, Yaw in degrees
                
                rx, ry, rz = euler_angles
                
                # Print pose information for all markers
                self.get_logger().info(f'Marker {i} - Position: x={pose.position.x:.3f}, y={pose.position.y:.3f}, z={pose.position.z:.3f}')
                self.get_logger().info(f'Marker {i} - Orientation (Euler): rx={rx:.2f}°, ry={ry:.2f}°, rz={rz:.2f}°')
                
                # Store data for plotting only for marker 3
                if i == 3:
                    marker_3_found = True
                    with self.data_lock:
                        self.time_data.append(current_time)
                        self.rx_data.append(rx)
                        self.ry_data.append(ry)
                        self.rz_data.append(rz)
                    
                    self.get_logger().info(f'Marker 3 data stored. Total points: {len(self.time_data)}')
                    
                    # Also save plots periodically
                    if current_time - self.last_plot_time > self.plot_interval:
                        self.save_plot_to_file()
                        self.last_plot_time = current_time
        
        # Log if marker 3 was not found
        if not marker_3_found and len(msg.poses) > 0:
            self.get_logger().info(f'Marker 3 not found. Available markers: {list(range(len(msg.poses)))}')
    
    def destroy_node(self):
        """Clean shutdown"""
        super().destroy_node()
    
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
        node.get_logger().info(f'Monitor orientation plots in {node.output_dir}/')
        node.get_logger().info(f'View latest plot with: eog {node.output_dir}/marker3_orientation_latest.png')
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()