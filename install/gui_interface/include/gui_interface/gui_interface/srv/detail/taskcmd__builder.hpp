// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from gui_interface:srv/Taskcmd.idl
// generated code does not contain a copyright notice

#ifndef GUI_INTERFACE__SRV__DETAIL__TASKCMD__BUILDER_HPP_
#define GUI_INTERFACE__SRV__DETAIL__TASKCMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "gui_interface/srv/detail/taskcmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace gui_interface
{

namespace srv
{

namespace builder
{

class Init_Taskcmd_Request_task
{
public:
  Init_Taskcmd_Request_task()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::gui_interface::srv::Taskcmd_Request task(::gui_interface::srv::Taskcmd_Request::_task_type arg)
  {
    msg_.task = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gui_interface::srv::Taskcmd_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::gui_interface::srv::Taskcmd_Request>()
{
  return gui_interface::srv::builder::Init_Taskcmd_Request_task();
}

}  // namespace gui_interface


namespace gui_interface
{

namespace srv
{

namespace builder
{

class Init_Taskcmd_Response_state
{
public:
  Init_Taskcmd_Response_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::gui_interface::srv::Taskcmd_Response state(::gui_interface::srv::Taskcmd_Response::_state_type arg)
  {
    msg_.state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::gui_interface::srv::Taskcmd_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::gui_interface::srv::Taskcmd_Response>()
{
  return gui_interface::srv::builder::Init_Taskcmd_Response_state();
}

}  // namespace gui_interface

#endif  // GUI_INTERFACE__SRV__DETAIL__TASKCMD__BUILDER_HPP_
