// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from gui_interface:srv/Taskcmd.idl
// generated code does not contain a copyright notice

#ifndef GUI_INTERFACE__SRV__DETAIL__TASKCMD__TRAITS_HPP_
#define GUI_INTERFACE__SRV__DETAIL__TASKCMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "gui_interface/srv/detail/taskcmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace gui_interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const Taskcmd_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: task
  {
    out << "task: ";
    rosidl_generator_traits::value_to_yaml(msg.task, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Taskcmd_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: task
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "task: ";
    rosidl_generator_traits::value_to_yaml(msg.task, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Taskcmd_Request & msg, bool use_flow_style = false)
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

}  // namespace gui_interface

namespace rosidl_generator_traits
{

[[deprecated("use gui_interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const gui_interface::srv::Taskcmd_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  gui_interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gui_interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const gui_interface::srv::Taskcmd_Request & msg)
{
  return gui_interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<gui_interface::srv::Taskcmd_Request>()
{
  return "gui_interface::srv::Taskcmd_Request";
}

template<>
inline const char * name<gui_interface::srv::Taskcmd_Request>()
{
  return "gui_interface/srv/Taskcmd_Request";
}

template<>
struct has_fixed_size<gui_interface::srv::Taskcmd_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<gui_interface::srv::Taskcmd_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<gui_interface::srv::Taskcmd_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace gui_interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const Taskcmd_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: state
  {
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Taskcmd_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: state
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "state: ";
    rosidl_generator_traits::value_to_yaml(msg.state, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Taskcmd_Response & msg, bool use_flow_style = false)
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

}  // namespace gui_interface

namespace rosidl_generator_traits
{

[[deprecated("use gui_interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const gui_interface::srv::Taskcmd_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  gui_interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use gui_interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const gui_interface::srv::Taskcmd_Response & msg)
{
  return gui_interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<gui_interface::srv::Taskcmd_Response>()
{
  return "gui_interface::srv::Taskcmd_Response";
}

template<>
inline const char * name<gui_interface::srv::Taskcmd_Response>()
{
  return "gui_interface/srv/Taskcmd_Response";
}

template<>
struct has_fixed_size<gui_interface::srv::Taskcmd_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<gui_interface::srv::Taskcmd_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<gui_interface::srv::Taskcmd_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<gui_interface::srv::Taskcmd>()
{
  return "gui_interface::srv::Taskcmd";
}

template<>
inline const char * name<gui_interface::srv::Taskcmd>()
{
  return "gui_interface/srv/Taskcmd";
}

template<>
struct has_fixed_size<gui_interface::srv::Taskcmd>
  : std::integral_constant<
    bool,
    has_fixed_size<gui_interface::srv::Taskcmd_Request>::value &&
    has_fixed_size<gui_interface::srv::Taskcmd_Response>::value
  >
{
};

template<>
struct has_bounded_size<gui_interface::srv::Taskcmd>
  : std::integral_constant<
    bool,
    has_bounded_size<gui_interface::srv::Taskcmd_Request>::value &&
    has_bounded_size<gui_interface::srv::Taskcmd_Response>::value
  >
{
};

template<>
struct is_service<gui_interface::srv::Taskcmd>
  : std::true_type
{
};

template<>
struct is_service_request<gui_interface::srv::Taskcmd_Request>
  : std::true_type
{
};

template<>
struct is_service_response<gui_interface::srv::Taskcmd_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // GUI_INTERFACE__SRV__DETAIL__TASKCMD__TRAITS_HPP_
