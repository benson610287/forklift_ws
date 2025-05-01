// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from docking_interface:srv/Dockingstatus.idl
// generated code does not contain a copyright notice

#ifndef DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__BUILDER_HPP_
#define DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "docking_interface/srv/detail/dockingstatus__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace docking_interface
{

namespace srv
{

namespace builder
{

class Init_Dockingstatus_Request_run
{
public:
  Init_Dockingstatus_Request_run()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::docking_interface::srv::Dockingstatus_Request run(::docking_interface::srv::Dockingstatus_Request::_run_type arg)
  {
    msg_.run = std::move(arg);
    return std::move(msg_);
  }

private:
  ::docking_interface::srv::Dockingstatus_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::docking_interface::srv::Dockingstatus_Request>()
{
  return docking_interface::srv::builder::Init_Dockingstatus_Request_run();
}

}  // namespace docking_interface


namespace docking_interface
{

namespace srv
{

namespace builder
{

class Init_Dockingstatus_Response_state
{
public:
  Init_Dockingstatus_Response_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::docking_interface::srv::Dockingstatus_Response state(::docking_interface::srv::Dockingstatus_Response::_state_type arg)
  {
    msg_.state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::docking_interface::srv::Dockingstatus_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::docking_interface::srv::Dockingstatus_Response>()
{
  return docking_interface::srv::builder::Init_Dockingstatus_Response_state();
}

}  // namespace docking_interface

#endif  // DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__BUILDER_HPP_
