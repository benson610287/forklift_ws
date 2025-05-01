// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from pallet_interfaces:msg/Boxinfo.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__MSG__DETAIL__BOXINFO__BUILDER_HPP_
#define PALLET_INTERFACES__MSG__DETAIL__BOXINFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "pallet_interfaces/msg/detail/boxinfo__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace pallet_interfaces
{

namespace msg
{

namespace builder
{

class Init_Boxinfo_height
{
public:
  explicit Init_Boxinfo_height(::pallet_interfaces::msg::Boxinfo & msg)
  : msg_(msg)
  {}
  ::pallet_interfaces::msg::Boxinfo height(::pallet_interfaces::msg::Boxinfo::_height_type arg)
  {
    msg_.height = std::move(arg);
    return std::move(msg_);
  }

private:
  ::pallet_interfaces::msg::Boxinfo msg_;
};

class Init_Boxinfo_width
{
public:
  explicit Init_Boxinfo_width(::pallet_interfaces::msg::Boxinfo & msg)
  : msg_(msg)
  {}
  Init_Boxinfo_height width(::pallet_interfaces::msg::Boxinfo::_width_type arg)
  {
    msg_.width = std::move(arg);
    return Init_Boxinfo_height(msg_);
  }

private:
  ::pallet_interfaces::msg::Boxinfo msg_;
};

class Init_Boxinfo_length
{
public:
  Init_Boxinfo_length()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Boxinfo_width length(::pallet_interfaces::msg::Boxinfo::_length_type arg)
  {
    msg_.length = std::move(arg);
    return Init_Boxinfo_width(msg_);
  }

private:
  ::pallet_interfaces::msg::Boxinfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::pallet_interfaces::msg::Boxinfo>()
{
  return pallet_interfaces::msg::builder::Init_Boxinfo_length();
}

}  // namespace pallet_interfaces

#endif  // PALLET_INTERFACES__MSG__DETAIL__BOXINFO__BUILDER_HPP_
