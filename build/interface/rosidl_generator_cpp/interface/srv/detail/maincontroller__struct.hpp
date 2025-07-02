// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interface:srv/Maincontroller.idl
// generated code does not contain a copyright notice

#ifndef INTERFACE__SRV__DETAIL__MAINCONTROLLER__STRUCT_HPP_
#define INTERFACE__SRV__DETAIL__MAINCONTROLLER__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__interface__srv__Maincontroller_Request __attribute__((deprecated))
#else
# define DEPRECATED__interface__srv__Maincontroller_Request __declspec(deprecated)
#endif

namespace interface
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Maincontroller_Request_
{
  using Type = Maincontroller_Request_<ContainerAllocator>;

  explicit Maincontroller_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->enable = false;
    }
  }

  explicit Maincontroller_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->enable = false;
    }
  }

  // field types and members
  using _enable_type =
    bool;
  _enable_type enable;

  // setters for named parameter idiom
  Type & set__enable(
    const bool & _arg)
  {
    this->enable = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interface::srv::Maincontroller_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const interface::srv::Maincontroller_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interface::srv::Maincontroller_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interface::srv::Maincontroller_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interface__srv__Maincontroller_Request
    std::shared_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interface__srv__Maincontroller_Request
    std::shared_ptr<interface::srv::Maincontroller_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Maincontroller_Request_ & other) const
  {
    if (this->enable != other.enable) {
      return false;
    }
    return true;
  }
  bool operator!=(const Maincontroller_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Maincontroller_Request_

// alias to use template instance with default allocator
using Maincontroller_Request =
  interface::srv::Maincontroller_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interface


#ifndef _WIN32
# define DEPRECATED__interface__srv__Maincontroller_Response __attribute__((deprecated))
#else
# define DEPRECATED__interface__srv__Maincontroller_Response __declspec(deprecated)
#endif

namespace interface
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Maincontroller_Response_
{
  using Type = Maincontroller_Response_<ContainerAllocator>;

  explicit Maincontroller_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->done = 0ll;
    }
  }

  explicit Maincontroller_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->done = 0ll;
    }
  }

  // field types and members
  using _done_type =
    int64_t;
  _done_type done;

  // setters for named parameter idiom
  Type & set__done(
    const int64_t & _arg)
  {
    this->done = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interface::srv::Maincontroller_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const interface::srv::Maincontroller_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interface::srv::Maincontroller_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interface::srv::Maincontroller_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interface__srv__Maincontroller_Response
    std::shared_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interface__srv__Maincontroller_Response
    std::shared_ptr<interface::srv::Maincontroller_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Maincontroller_Response_ & other) const
  {
    if (this->done != other.done) {
      return false;
    }
    return true;
  }
  bool operator!=(const Maincontroller_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Maincontroller_Response_

// alias to use template instance with default allocator
using Maincontroller_Response =
  interface::srv::Maincontroller_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace interface

namespace interface
{

namespace srv
{

struct Maincontroller
{
  using Request = interface::srv::Maincontroller_Request;
  using Response = interface::srv::Maincontroller_Response;
};

}  // namespace srv

}  // namespace interface

#endif  // INTERFACE__SRV__DETAIL__MAINCONTROLLER__STRUCT_HPP_
