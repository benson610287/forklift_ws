// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from docking_interface:srv/Dockingstatus.idl
// generated code does not contain a copyright notice

#ifndef DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__TRAITS_HPP_
#define DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "docking_interface/srv/detail/dockingstatus__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace docking_interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const Dockingstatus_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: run
  {
    out << "run: ";
    rosidl_generator_traits::value_to_yaml(msg.run, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Dockingstatus_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: run
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "run: ";
    rosidl_generator_traits::value_to_yaml(msg.run, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Dockingstatus_Request & msg, bool use_flow_style = false)
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

}  // namespace docking_interface

namespace rosidl_generator_traits
{

[[deprecated("use docking_interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const docking_interface::srv::Dockingstatus_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  docking_interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use docking_interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const docking_interface::srv::Dockingstatus_Request & msg)
{
  return docking_interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<docking_interface::srv::Dockingstatus_Request>()
{
  return "docking_interface::srv::Dockingstatus_Request";
}

template<>
inline const char * name<docking_interface::srv::Dockingstatus_Request>()
{
  return "docking_interface/srv/Dockingstatus_Request";
}

template<>
struct has_fixed_size<docking_interface::srv::Dockingstatus_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<docking_interface::srv::Dockingstatus_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<docking_interface::srv::Dockingstatus_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace docking_interface
{

namespace srv
{

inline void to_flow_style_yaml(
  const Dockingstatus_Response & msg,
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
  const Dockingstatus_Response & msg,
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

inline std::string to_yaml(const Dockingstatus_Response & msg, bool use_flow_style = false)
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

}  // namespace docking_interface

namespace rosidl_generator_traits
{

[[deprecated("use docking_interface::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const docking_interface::srv::Dockingstatus_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  docking_interface::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use docking_interface::srv::to_yaml() instead")]]
inline std::string to_yaml(const docking_interface::srv::Dockingstatus_Response & msg)
{
  return docking_interface::srv::to_yaml(msg);
}

template<>
inline const char * data_type<docking_interface::srv::Dockingstatus_Response>()
{
  return "docking_interface::srv::Dockingstatus_Response";
}

template<>
inline const char * name<docking_interface::srv::Dockingstatus_Response>()
{
  return "docking_interface/srv/Dockingstatus_Response";
}

template<>
struct has_fixed_size<docking_interface::srv::Dockingstatus_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<docking_interface::srv::Dockingstatus_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<docking_interface::srv::Dockingstatus_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<docking_interface::srv::Dockingstatus>()
{
  return "docking_interface::srv::Dockingstatus";
}

template<>
inline const char * name<docking_interface::srv::Dockingstatus>()
{
  return "docking_interface/srv/Dockingstatus";
}

template<>
struct has_fixed_size<docking_interface::srv::Dockingstatus>
  : std::integral_constant<
    bool,
    has_fixed_size<docking_interface::srv::Dockingstatus_Request>::value &&
    has_fixed_size<docking_interface::srv::Dockingstatus_Response>::value
  >
{
};

template<>
struct has_bounded_size<docking_interface::srv::Dockingstatus>
  : std::integral_constant<
    bool,
    has_bounded_size<docking_interface::srv::Dockingstatus_Request>::value &&
    has_bounded_size<docking_interface::srv::Dockingstatus_Response>::value
  >
{
};

template<>
struct is_service<docking_interface::srv::Dockingstatus>
  : std::true_type
{
};

template<>
struct is_service_request<docking_interface::srv::Dockingstatus_Request>
  : std::true_type
{
};

template<>
struct is_service_response<docking_interface::srv::Dockingstatus_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__TRAITS_HPP_
