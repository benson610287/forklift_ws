// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from pallet_interfaces:srv/Palletstate.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__STRUCT_HPP_
#define PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__pallet_interfaces__srv__Palletstate_Request __attribute__((deprecated))
#else
# define DEPRECATED__pallet_interfaces__srv__Palletstate_Request __declspec(deprecated)
#endif

namespace pallet_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Palletstate_Request_
{
  using Type = Palletstate_Request_<ContainerAllocator>;

  explicit Palletstate_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->run = false;
    }
  }

  explicit Palletstate_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->run = false;
    }
  }

  // field types and members
  using _run_type =
    bool;
  _run_type run;

  // setters for named parameter idiom
  Type & set__run(
    const bool & _arg)
  {
    this->run = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pallet_interfaces__srv__Palletstate_Request
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pallet_interfaces__srv__Palletstate_Request
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Palletstate_Request_ & other) const
  {
    if (this->run != other.run) {
      return false;
    }
    return true;
  }
  bool operator!=(const Palletstate_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Palletstate_Request_

// alias to use template instance with default allocator
using Palletstate_Request =
  pallet_interfaces::srv::Palletstate_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pallet_interfaces


#ifndef _WIN32
# define DEPRECATED__pallet_interfaces__srv__Palletstate_Response __attribute__((deprecated))
#else
# define DEPRECATED__pallet_interfaces__srv__Palletstate_Response __declspec(deprecated)
#endif

namespace pallet_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Palletstate_Response_
{
  using Type = Palletstate_Response_<ContainerAllocator>;

  explicit Palletstate_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0ll;
    }
  }

  explicit Palletstate_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0ll;
    }
  }

  // field types and members
  using _state_type =
    int64_t;
  _state_type state;

  // setters for named parameter idiom
  Type & set__state(
    const int64_t & _arg)
  {
    this->state = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__pallet_interfaces__srv__Palletstate_Response
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__pallet_interfaces__srv__Palletstate_Response
    std::shared_ptr<pallet_interfaces::srv::Palletstate_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Palletstate_Response_ & other) const
  {
    if (this->state != other.state) {
      return false;
    }
    return true;
  }
  bool operator!=(const Palletstate_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Palletstate_Response_

// alias to use template instance with default allocator
using Palletstate_Response =
  pallet_interfaces::srv::Palletstate_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace pallet_interfaces

namespace pallet_interfaces
{

namespace srv
{

struct Palletstate
{
  using Request = pallet_interfaces::srv::Palletstate_Request;
  using Response = pallet_interfaces::srv::Palletstate_Response;
};

}  // namespace srv

}  // namespace pallet_interfaces

#endif  // PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__STRUCT_HPP_
