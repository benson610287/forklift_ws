// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pallet_interfaces:msg/Boxinfo.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__MSG__DETAIL__BOXINFO__TRAITS_HPP_
#define PALLET_INTERFACES__MSG__DETAIL__BOXINFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pallet_interfaces/msg/detail/boxinfo__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pallet_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const Boxinfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: length
  {
    out << "length: ";
    rosidl_generator_traits::value_to_yaml(msg.length, out);
    out << ", ";
  }

  // member: width
  {
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << ", ";
  }

  // member: height
  {
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Boxinfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: length
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "length: ";
    rosidl_generator_traits::value_to_yaml(msg.length, out);
    out << "\n";
  }

  // member: width
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "width: ";
    rosidl_generator_traits::value_to_yaml(msg.width, out);
    out << "\n";
  }

  // member: height
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "height: ";
    rosidl_generator_traits::value_to_yaml(msg.height, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Boxinfo & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace pallet_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pallet_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pallet_interfaces::msg::Boxinfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  pallet_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pallet_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const pallet_interfaces::msg::Boxinfo & msg)
{
  return pallet_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<pallet_interfaces::msg::Boxinfo>()
{
  return "pallet_interfaces::msg::Boxinfo";
}

template<>
inline const char * name<pallet_interfaces::msg::Boxinfo>()
{
  return "pallet_interfaces/msg/Boxinfo";
}

template<>
struct has_fixed_size<pallet_interfaces::msg::Boxinfo>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pallet_interfaces::msg::Boxinfo>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pallet_interfaces::msg::Boxinfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // PALLET_INTERFACES__MSG__DETAIL__BOXINFO__TRAITS_HPP_
