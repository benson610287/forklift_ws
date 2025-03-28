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

class Init_Maincontroller_Request_enable
{
public:
  Init_Maincontroller_Request_enable()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interface::srv::Maincontroller_Request enable(::interface::srv::Maincontroller_Request::_enable_type arg)
  {
    msg_.enable = std::move(arg);
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
  return interface::srv::builder::Init_Maincontroller_Request_enable();
}

}  // namespace interface


namespace interface
{

namespace srv
{

namespace builder
{

class Init_Maincontroller_Response_done
{
public:
  Init_Maincontroller_Response_done()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interface::srv::Maincontroller_Response done(::interface::srv::Maincontroller_Response::_done_type arg)
  {
    msg_.done = std::move(arg);
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
  return interface::srv::builder::Init_Maincontroller_Response_done();
}

}  // namespace interface

#endif  // INTERFACE__SRV__DETAIL__MAINCONTROLLER__BUILDER_HPP_
