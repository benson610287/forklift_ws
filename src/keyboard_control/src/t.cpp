#include "rclcpp/rclcpp.hpp"
// #include "std_msgs/msg/String.h"
#include <geometry_msgs/msg/twist.hpp>
#include <sstream>
#include<iostream>
#include "std_msgs/msg/int64.hpp"

#include "interface/srv/slidecmd.hpp"

#include <conio.h>

int main(int argc, char **argv)
{
 
  // ros::init(argc, argv, "talker");
 
  Console C;
  // int ch;
  // ros::NodeHandle mobile;
  // ros::NodeHandle slide;
  // ros::Publisher mobile_pub = mobile.advertise<geometry_msgs::Twist>("mobile/cmd_vel", 1000);
  // ros::Publisher slide_pub = slide.advertise<std_msgs::Int64>("topic", 1000);
  // ros::Rate loop_rate(10);
  char c;
  // geometry_msgs::Twist msg_mobile;
  // std_msgs::Int64 msg_slide;
  


  rclcpp::init(argc, argv);
  auto node = rclcpp::Node::make_shared("talker");  
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr mobile_pub;
  rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr slide_pub;

  rclcpp::Client<interface::srv::Slidecmd>::SharedPtr client =
    node->create_client<interface::srv::Slidecmd>("linear/move_cmd");
  
  


  mobile_pub = node->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 1000);
  slide_pub = node->create_publisher<std_msgs::msg::Int64>("linear/move_cmd", 1000);

  std::shared_ptr<rclcpp::Rate> loop_rate = std::make_shared<rclcpp::Rate>(10);
  geometry_msgs::msg::Twist msg_mobile;
  std_msgs::msg::Int64 msg_slide;

  auto slide_request = std::make_shared<interface::srv::Slidecmd::Request>();

  msg_mobile.linear.x=0;
  msg_mobile.linear.y=0;
  msg_mobile.linear.z=0;
  msg_mobile.angular.x=0;
  msg_mobile.angular.y=0;
  msg_mobile.angular.z=0;
  msg_slide.data=0;
  slide_request->pos=0;

    while(rclcpp::ok())
    {
       c = C.getche();
      if(c=='w')
      {
        msg_mobile.linear.x+=0.1;
        std::cout<<std::endl<<"x_speed:"<<msg_mobile.linear.x<<std::endl;
        std::cout<<"y_speed:"<<msg_mobile.linear.y<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::Duration(0.5).sleep();
        // ros::spinOnce();
        loop_rate->sleep();
      }else if(c=='a'){
        msg_mobile.linear.y+=0.1;
        std::cout<<std::endl<<"x_speed:"<<msg_mobile.linear.x<<std::endl;
        std::cout<<"y_speed:"<<msg_mobile.linear.y<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::spinOnce();
      }else if(c=='s'){
        msg_mobile.linear.x=0;
        msg_mobile.linear.y=0;
        msg_mobile.linear.z=0;
        msg_mobile.angular.x=0;
        msg_mobile.angular.y=0;
        msg_mobile.angular.z=0;
        std::cout<<std::endl<<"x_speed:"<<msg_mobile.linear.x<<std::endl;
        std::cout<<"y_speed:"<<msg_mobile.linear.y<<std::endl;
        std::cout<<"y_speed:"<<msg_mobile.angular.z<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::spinOnce();
      }else if(c=='d'){
        msg_mobile.linear.y-=0.1;
        std::cout<<std::endl<<"x_speed:"<<msg_mobile.linear.x<<std::endl;
        std::cout<<"y_speed:"<<msg_mobile.linear.y<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::spinOnce();
      }else if(c=='x'){
        msg_mobile.linear.x-=0.1;
        std::cout<<std::endl<<"x_speed:"<<msg_mobile.linear.x<<std::endl;
        std::cout<<"y_speed:"<<msg_mobile.linear.y<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::spinOnce();
      }else if(c=='z'){
        msg_mobile.angular.z+=0.1;
        std::cout<<std::endl<<"angular_z:"<<msg_mobile.angular.z<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::spinOnce();
      }else if(c=='c'){
        msg_mobile.angular.z-=0.1;
        std::cout<<std::endl<<"angular_z:"<<msg_mobile.angular.z<<std::endl;
        mobile_pub->publish(msg_mobile);
        // ros::spinOnce();
      }else if(c=='q'){  //up
        slide_request->pos+=5;
        // msg_slide.data+=5;
        std::cout<<std::endl<<"slide_pos:"<<slide_request->pos<<std::endl;
        auto result = client->async_send_request(slide_request);
        if (rclcpp::spin_until_future_complete(node, result) ==
          rclcpp::FutureReturnCode::SUCCESS)
        {
          if (result.get()->done){
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "SUCCESS");
          }else{
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "SUCCESS but fail");
          }
          

        } else {
          RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service add_two_ints");
        }
        // slide_pub->publish(msg_slide);
        // ros::spinOnce();
      }else if(c=='e'){  //down
        slide_request->pos-=5;
        // msg_slide.data-=5;
        std::cout<<std::endl<<"slide_pos:"<<slide_request->pos<<std::endl;
        auto result = client->async_send_request(slide_request);
        if (rclcpp::spin_until_future_complete(node, result) ==
          rclcpp::FutureReturnCode::SUCCESS)
        {
          if (result.get()->done){
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "SUCCESS");
          }else{
            RCLCPP_INFO(rclcpp::get_logger("rclcpp"), "SUCCESS but fail");
          }
        } else {
          RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Failed to call service add_two_ints");
        }
        // slide_pub->publish(msg_slide);
        // ros::spinOnce();
      }


    }

  std::cin.sync();              
  std::cin.get(); 
  

  // /**
  //  * A count of how many messages we have sent. This is used to create
  //  * a unique string for each message.
  //  */
  // int count = 0;
  // while (ros::ok())
  // {

  //   // geometry_msgs::Twist msg;
  //   if (C.kbhit()){
  //       ch = getchar();//使用_getch()函数获取按下的键值  119 97 115 100
  //       std::cout << ch;
  //       // if
  //       ROS_INFO("aaa");
  //   }
  //   // msg.data = ss.str();
  //   // std::cout<<"x=";
  //   // std::cin>>msg.linear.x;
  //   // std::cout<<"x=";
  //   // std::cin>>msg.linear.x;
  //   // std::cout<<"x=";
  //   // std::cin>>msg.linear.x;
  //   // ROS_INFO("%s", msg.data.c_str());


  //   // chatter_pub.publish(msg);

  //   ros::spinOnce();

  //   loop_rate.sleep();
  //   ++count;
  // }


  return 0;
}

