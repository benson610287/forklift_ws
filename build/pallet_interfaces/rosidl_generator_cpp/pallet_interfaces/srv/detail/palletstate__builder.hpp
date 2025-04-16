// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pallet_interfaces:srv/Palletstate.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__BUILDER_HPP_
#define PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pallet_interfaces/srv/detail/palletstate__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pallet_interfaces
{

namespace srv
{

namespace builder
{

class Init_Palletstate_Request_run
{
public:
  Init_Palletstate_Request_run()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::pallet_interfaces::srv::Palletstate_Request run(::pallet_interfaces::srv::Palletstate_Request::_run_type arg)
  {
    msg_.run = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pallet_interfaces::srv::Palletstate_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pallet_interfaces::srv::Palletstate_Request>()
{
  return pallet_interfaces::srv::builder::Init_Palletstate_Request_run();
}

}  // namespace pallet_interfaces


namespace pallet_interfaces
{

namespace srv
{

namespace builder
{

class Init_Palletstate_Response_state
{
public:
  Init_Palletstate_Response_state()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::pallet_interfaces::srv::Palletstate_Response state(::pallet_interfaces::srv::Palletstate_Response::_state_type arg)
  {
    msg_.state = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pallet_interfaces::srv::Palletstate_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::pallet_interfaces::srv::Palletstate_Response>()
{
  return pallet_interfaces::srv::builder::Init_Palletstate_Response_state();
}

}  // namespace pallet_interfaces

#endif  // PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__BUILDER_HPP_
