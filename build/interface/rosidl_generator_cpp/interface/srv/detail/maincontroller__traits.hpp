// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interface:srv/Maincontroller.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__SRV__DETAIL__MAINCONTROLLER__TRAITS_HPP_
#define INTERFACE__SRV__DETAIL__MAINCONTROLLER__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "interface/srv/detail/maincontroller__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const Maincontroller_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: a
  {
    out << "a: ";
    rosidl_generator_traits::value_to_yaml(msg.a, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Maincontroller_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: a
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "a: ";
    rosidl_generator_traits::value_to_yaml(msg.a, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Maincontroller_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace interface

namespace rosidl_generator_traits
{

[[deprecated("use interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interface::srv::Maincontroller_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const interface::srv::Maincontroller_Request & msg)
{
  return interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<interface::srv::Maincontroller_Request>()
{
  return "interface::srv::Maincontroller_Request";
}

template<>
inline const char * name<interface::srv::Maincontroller_Request>()
{
  return "interface/srv/Maincontroller_Request";
}

template<>
struct has_fixed_size<interface::srv::Maincontroller_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interface::srv::Maincontroller_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interface::srv::Maincontroller_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const Maincontroller_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: sum
  {
    out << "sum: ";
    rosidl_generator_traits::value_to_yaml(msg.sum, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Maincontroller_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: sum
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sum: ";
    rosidl_generator_traits::value_to_yaml(msg.sum, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Maincontroller_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace interface

namespace rosidl_generator_traits
{

[[deprecated("use interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const interface::srv::Maincontroller_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const interface::srv::Maincontroller_Response & msg)
{
  return interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<interface::srv::Maincontroller_Response>()
{
  return "interface::srv::Maincontroller_Response";
}

template<>
inline const char * name<interface::srv::Maincontroller_Response>()
{
  return "interface/srv/Maincontroller_Response";
}

template<>
struct has_fixed_size<interface::srv::Maincontroller_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interface::srv::Maincontroller_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interface::srv::Maincontroller_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interface::srv::Maincontroller>()
{
  return "interface::srv::Maincontroller";
}

template<>
inline const char * name<interface::srv::Maincontroller>()
{
  return "interface/srv/Maincontroller";
}

template<>
struct has_fixed_size<interface::srv::Maincontroller>
  : std::integral_constant<
    bool,
    has_fixed_size<interface::srv::Maincontroller_Request>::value &&
    has_fixed_size<interface::srv::Maincontroller_Response>::value
  >
{
};

template<>
struct has_bounded_size<interface::srv::Maincontroller>
  : std::integral_constant<
    bool,
    has_bounded_size<interface::srv::Maincontroller_Request>::value &&
    has_bounded_size<interface::srv::Maincontroller_Response>::value
  >
{
};

template<>
struct is_service<interface::srv::Maincontroller>
  : std::true_type
{
};

template<>
struct is_service_request<interface::srv::Maincontroller_Request>
  : std::true_type
{
};

template<>
struct is_service_response<interface::srv::Maincontroller_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // INTERFACE__SRV__DETAIL__MAINCONTROLLER__TRAITS_HPP_
