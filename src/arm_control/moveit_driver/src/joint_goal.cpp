

#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

#include <geometry_msgs/msg/pose.hpp>
#include "interface/srv/armcontrolangle.hpp"
#include <tf2/LinearMath/Quaternion.h>
// Create a ROS logger
auto const logger = rclcpp::get_logger("joint_goal");
// Global node pointer (used in callback)
rclcpp::Node::SharedPtr node;

void add(const std::shared_ptr<interface::srv::Armcontrolangle::Request>   request,
          std::shared_ptr<interface::srv::Armcontrolangle::Response>      response)
{
  // ...existing code...
  RCLCPP_INFO(logger, "-------------------------------------");
  // Create the MoveIt Move Group Interface
  using moveit::planning_interface::MoveGroupInterface;
  auto move_group_interface = MoveGroupInterface(node, "ur_manipulator");

  // Method 1: Set individual joint values
  std::vector<double> joint_group_positions = {
    request->joint.data[0],  // Joint 1 position in radians
    request->joint.data[1],  // Joint 2 position in radians
    request->joint.data[2],  // Joint 3 position in radians
    request->joint.data[3],  // Joint 4 position in radians
    request->joint.data[4],  // Joint 5 position in radians
    request->joint.data[5],  // Joint 6 position in radians
  };
  
  move_group_interface.setJointValueTarget(joint_group_positions);

  // Method 2: Set joint values by name
  // move_group_interface.setJointValueTarget("shoulder_pan_joint", joint1_value);
  // move_group_interface.setJointValueTarget("shoulder_lift_joint", joint2_value);
  // move_group_interface.setJointValueTarget("elbow_joint", joint3_value);
  // move_group_interface.setJointValueTarget("wrist_1_joint", joint4_value);
  // move_group_interface.setJointValueTarget("wrist_2_joint", joint5_value);
  // move_group_interface.setJointValueTarget("wrist_3_joint", joint6_value);

  // Plan and execute
  moveit::planning_interface::MoveGroupInterface::Plan my_plan;
  bool success = (move_group_interface.plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);

  if(success) {
    move_group_interface.execute(my_plan);
    response->status = 1;
    RCLCPP_INFO(logger, "Joint motion executed successfully");
  } else {
    RCLCPP_ERROR(logger, "Joint planning failed!");
    response->status = -1;
  }

  RCLCPP_INFO(logger, "sending back response: [%ld]", response->status);
}




int main(int argc, char * argv[])
{
  // Initialize ROS and create the Node
  rclcpp::init(argc, argv);
  node = std::make_shared<rclcpp::Node>("joint_goal");



  geometry_msgs::msg::Pose target_pose;

  rclcpp::Service<interface::srv::Armcontrolangle>::SharedPtr service = node->create_service<interface::srv::Armcontrolangle>("joint_arm_cmd", &add);


  // Shutdown
  RCLCPP_INFO(logger, "Ready to receive pose commands.");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
