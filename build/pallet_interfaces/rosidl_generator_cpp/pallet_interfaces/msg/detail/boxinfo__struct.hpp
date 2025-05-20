// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pallet_interfaces:msg/Boxinfo.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__MSG__DETAIL__BOXINFO__STRUCT_HPP_
#define PALLET_INTERFACES__MSG__DETAIL__BOXINFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pallet_interfaces__msg__Boxinfo __attribute__((deprecated))
#else
# define DEPRECATED__pallet_interfaces__msg__Boxinfo __declspec(deprecated)
#endif

namespace pallet_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Boxinfo_
{
  using Type = Boxinfo_<ContainerAllocator>;

  explicit Boxinfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->length = 0.0;
      this->width = 0.0;
      this->height = 0.0;
    }
  }

  explicit Boxinfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->length = 0.0;
      this->width = 0.0;
      this->height = 0.0;
    }
  }

  // field types and members
  using _length_type =
    double;
  _length_type length;
  using _width_type =
    double;
  _width_type width;
  using _height_type =
    double;
  _height_type height;

  // setters for named parameter idiom
  Type & set__length(
    const double & _arg)
  {
    this->length = _arg;
    return *this;
  }
  Type & set__width(
    const double & _arg)
  {
    this->width = _arg;
    return *this;
  }
  Type & set__height(
    const double & _arg)
  {
    this->height = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pallet_interfaces::msg::Boxinfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const pallet_interfaces::msg::Boxinfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pallet_interfaces::msg::Boxinfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pallet_interfaces::msg::Boxinfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pallet_interfaces__msg__Boxinfo
    std::shared_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pallet_interfaces__msg__Boxinfo
    std::shared_ptr<pallet_interfaces::msg::Boxinfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Boxinfo_ & other) const
  {
    if (this->length != other.length) {
      return false;
    }
    if (this->width != other.width) {
      return false;
    }
    if (this->height != other.height) {
      return false;
    }
    return true;
  }
  bool operator!=(const Boxinfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Boxinfo_

// alias to use template instance with default allocator
using Boxinfo =
  pallet_interfaces::msg::Boxinfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace pallet_interfaces

#endif  // PALLET_INTERFACES__MSG__DETAIL__BOXINFO__STRUCT_HPP_
