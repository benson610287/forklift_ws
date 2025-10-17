

#include <memory>

#include <rclcpp/rclcpp.hpp>
#include <moveit/move_group_interface/move_group_interface.h>

#include <geometry_msgs/msg/pose.hpp>
#include "interface/srv/armcontrol.hpp"
#include <tf2/LinearMath/Quaternion.h>
// Create a ROS logger
auto const logger = rclcpp::get_logger("line_goal");
// Global node pointer (used in callback)
rclcpp::Node::SharedPtr node;

void add(const std::shared_ptr<interface::srv::Armcontrol::Request>   request,
          std::shared_ptr<interface::srv::Armcontrol::Response>      response)
{
  // response->sum = request->a + request->b;
  RCLCPP_INFO(logger, "Incoming request\n"
                      "position.x: %f  y: %f  z: %f\n"
                      "orientation.x: %f  y: %f  z: %f  w: %f",
              request->pose.position.x, request->pose.position.y, request->pose.position.z,
              request->pose.orientation.x, request->pose.orientation.y,
              request->pose.orientation.z, request->pose.orientation.w);
  // RCLCPP_INFO(logger, "sending back response: [%ld]", response->status);
  






  tf2::Quaternion q(
  request->pose.orientation.x,
  request->pose.orientation.y,
  request->pose.orientation.z,
  request->pose.orientation.w
  );
  q.normalize();

  

  // Create the MoveIt Move Group Interface for panda arm
  using moveit::planning_interface::MoveGroupInterface;
  auto move_group_interface = MoveGroupInterface(node, "ur_manipulator");
  // Create a target Pose for the end-effector

  request->pose.position.x*=-1;
  request->pose.position.y*=-1;
  geometry_msgs::msg::Pose target_pose;
  target_pose.position=request->pose.position;
  target_pose.orientation.x = q.x();
  target_pose.orientation.y = q.y();
  target_pose.orientation.z = q.z();
  target_pose.orientation.w = q.w();



  // move_group_interface.setPoseTarget(target_pose);

  // // Create a plan to that target pose and check if that plan is successful
  // moveit::planning_interface::MoveGroupInterface::Plan my_plan;
  // bool success = (move_group_interface.plan(my_plan) == moveit::core::MoveItErrorCode::SUCCESS);

  // // If the plan is successful, execute the plan
  // if(success) {
  //   move_group_interface.execute(my_plan);
  //   response->status=1;
  // } else {
  //   RCLCPP_ERROR(logger, "Planing failed!");
  //   response->status=-1;
  // }

  // Create waypoints for Cartesian path
  std::vector<geometry_msgs::msg::Pose> waypoints;
  waypoints.push_back(target_pose);  // Add your target pose

  // Cartesian path parameters
  moveit_msgs::msg::RobotTrajectory trajectory;
  const double eef_step = 0.01;       // 1cm step size
  const double jump_threshold = 0.0;  // Disable jump threshold

  // Compute Cartesian path (straight line from current pose to target)
  double fraction = move_group_interface.computeCartesianPath(
      waypoints,
      eef_step,
      jump_threshold,
      trajectory
  );

  RCLCPP_INFO(logger, "Cartesian path planned (%.2f%% achieved)", fraction * 100.0);

  // Execute if path planning was successful
  if (fraction >= 0.95) {  // 95% of path achieved
    moveit::planning_interface::MoveGroupInterface::Plan cartesian_plan;
    cartesian_plan.trajectory_ = trajectory;
    
    bool success = move_group_interface.execute(cartesian_plan) == moveit::core::MoveItErrorCode::SUCCESS;
    response->status = success ? 1 : -1;
  } else {
    RCLCPP_ERROR(logger, "Cartesian path planning failed! Only %.2f%% achieved", fraction * 100.0);
    response->status = -1;
  }


  RCLCPP_INFO(logger, "sending back response: [%ld]", response->status);
}




int main(int argc, char * argv[])
{
  // Initialize ROS and create the Node
  rclcpp::init(argc, argv);
  node = std::make_shared<rclcpp::Node>("line_goal");

  

  // Create the MoveIt Move Group Interface for panda arm
  // using moveit::planning_interface::MoveGroupInterface;
  // auto move_group_interface = MoveGroupInterface(node, "ur_manipulator");

  // Create a target Pose for the end-effector
  

  geometry_msgs::msg::Pose target_pose;

  rclcpp::Service<interface::srv::Armcontrol>::SharedPtr service = node->create_service<interface::srv::Armcontrol>("line_arm_cmd", &add);

  //ex pose
  target_pose.orientation.x=-0.707;
  target_pose.orientation.y=0.707;
  target_pose.orientation.z=0;
  target_pose.orientation.w=0;
// target_pose.position.x=-100
// target_pose.position.y=-550
// target_pose.position.z=500


  // std::cout<<"target_pose.orientation.x=";
  // std::cin>>target_pose.orientation.x;
  // std::cout<<"target_pose.orientation.y=";
  // std::cin>>target_pose.orientation.y;
  // std::cout<<"target_pose.orientation.z=";
  // std::cin>>target_pose.orientation.z;
  // std::cout<<"target_pose.orientation.w=";
  // std::cin>>target_pose.orientation.w;
  // std::cout<<"target_pose.position.x=";
  // std::cin>>target_pose.position.x;
  // std::cout<<"target_pose.position.y=";
  // std::cin>>target_pose.position.y;
  // std::cout<<"target_pose.position.z=";
  // std::cin>>target_pose.position.z;
  // target_pose.position.x*=-0.001;
  // target_pose.position.y*=-0.001;
  // target_pose.position.z*=0.001;
  // Set the target pose
  


  // using moveit::planning_interface::MoveGroupInterface;
  // auto move_group_interface = MoveGroupInterface(node, "ur_manipulator");
  // geometry_msgs::msg::PoseStamped current_pose = move_group_interface.getCurrentPose();
  // RCLCPP_INFO_STREAM(logger, "Current EE Position: x=" << current_pose.pose.position.x
  //                     << ", y=" << current_pose.pose.position.y
  //                     << ", z=" << current_pose.pose.position.z);
  // RCLCPP_INFO_STREAM(logger, "Orientation (quaternion): x=" << current_pose.pose.orientation.x
  //                     << ", y=" << current_pose.pose.orientation.y
  //                     << ", z=" << current_pose.pose.orientation.z
  //                     << ", w=" << current_pose.pose.orientation.w);

  // Shutdown
  RCLCPP_INFO(logger, "Ready to receive pose commands.");
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
