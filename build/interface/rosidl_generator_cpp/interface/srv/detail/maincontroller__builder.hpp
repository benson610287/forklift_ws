// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interface:srv/Maincontroller.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__SRV__DETAIL__MAINCONTROLLER__BUILDER_HPP_
#define INTERFACE__SRV__DETAIL__MAINCONTROLLER__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "interface/srv/detail/maincontroller__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace interface
{

namespace srv
{

namespace builder
{

class Init_Maincontroller_Request_a
{
public:
  Init_Maincontroller_Request_a()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interface::srv::Maincontroller_Request a(::interface::srv::Maincontroller_Request::_a_type arg)
  {
    msg_.a = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interface::srv::Maincontroller_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface::srv::Maincontroller_Request>()
{
  return interface::srv::builder::Init_Maincontroller_Request_a();
}

}  // namespace interface


namespace interface
{

namespace srv
{

namespace builder
{

class Init_Maincontroller_Response_sum
{
public:
  Init_Maincontroller_Response_sum()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interface::srv::Maincontroller_Response sum(::interface::srv::Maincontroller_Response::_sum_type arg)
  {
    msg_.sum = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interface::srv::Maincontroller_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::interface::srv::Maincontroller_Response>()
{
  return interface::srv::builder::Init_Maincontroller_Response_sum();
}

}  // namespace interface

#endif  // INTERFACE__SRV__DETAIL__MAINCONTROLLER__BUILDER_HPP_
