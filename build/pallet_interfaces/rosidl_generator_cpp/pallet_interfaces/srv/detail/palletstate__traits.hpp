// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from pallet_interfaces:srv/Palletstate.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__TRAITS_HPP_
#define PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "pallet_interfaces/srv/detail/palletstate__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace pallet_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Palletstate_Request & msg,
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
  const Palletstate_Request & msg,
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

inline std::string to_yaml(const Palletstate_Request & msg, bool use_flow_style = false)
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

}  // namespace pallet_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pallet_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pallet_interfaces::srv::Palletstate_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  pallet_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pallet_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pallet_interfaces::srv::Palletstate_Request & msg)
{
  return pallet_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pallet_interfaces::srv::Palletstate_Request>()
{
  return "pallet_interfaces::srv::Palletstate_Request";
}

template<>
inline const char * name<pallet_interfaces::srv::Palletstate_Request>()
{
  return "pallet_interfaces/srv/Palletstate_Request";
}

template<>
struct has_fixed_size<pallet_interfaces::srv::Palletstate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pallet_interfaces::srv::Palletstate_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pallet_interfaces::srv::Palletstate_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace pallet_interfaces
{

namespace srv
{

inline void to_flow_style_yaml(
  const Palletstate_Response & msg,
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
  const Palletstate_Response & msg,
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

inline std::string to_yaml(const Palletstate_Response & msg, bool use_flow_style = false)
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

}  // namespace pallet_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use pallet_interfaces::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const pallet_interfaces::srv::Palletstate_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  pallet_interfaces::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use pallet_interfaces::srv::to_yaml() instead")]]
inline std::string to_yaml(const pallet_interfaces::srv::Palletstate_Response & msg)
{
  return pallet_interfaces::srv::to_yaml(msg);
}

template<>
inline const char * data_type<pallet_interfaces::srv::Palletstate_Response>()
{
  return "pallet_interfaces::srv::Palletstate_Response";
}

template<>
inline const char * name<pallet_interfaces::srv::Palletstate_Response>()
{
  return "pallet_interfaces/srv/Palletstate_Response";
}

template<>
struct has_fixed_size<pallet_interfaces::srv::Palletstate_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<pallet_interfaces::srv::Palletstate_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<pallet_interfaces::srv::Palletstate_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<pallet_interfaces::srv::Palletstate>()
{
  return "pallet_interfaces::srv::Palletstate";
}

template<>
inline const char * name<pallet_interfaces::srv::Palletstate>()
{
  return "pallet_interfaces/srv/Palletstate";
}

template<>
struct has_fixed_size<pallet_interfaces::srv::Palletstate>
  : std::integral_constant<
    bool,
    has_fixed_size<pallet_interfaces::srv::Palletstate_Request>::value &&
    has_fixed_size<pallet_interfaces::srv::Palletstate_Response>::value
  >
{
};

template<>
struct has_bounded_size<pallet_interfaces::srv::Palletstate>
  : std::integral_constant<
    bool,
    has_bounded_size<pallet_interfaces::srv::Palletstate_Request>::value &&
    has_bounded_size<pallet_interfaces::srv::Palletstate_Response>::value
  >
{
};

template<>
struct is_service<pallet_interfaces::srv::Palletstate>
  : std::true_type
{
};

template<>
struct is_service_request<pallet_interfaces::srv::Palletstate_Request>
  : std::true_type
{
};

template<>
struct is_service_response<pallet_interfaces::srv::Palletstate_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__TRAITS_HPP_
