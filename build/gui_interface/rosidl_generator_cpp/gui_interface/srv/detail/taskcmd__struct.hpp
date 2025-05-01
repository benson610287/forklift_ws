// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from gui_interface:srv/Taskcmd.idl
// generated code does not contain a copyright notice

#ifndef GUI_INTERFACE__SRV__DETAIL__TASKCMD__STRUCT_HPP_
#define GUI_INTERFACE__SRV__DETAIL__TASKCMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__gui_interface__srv__Taskcmd_Request __attribute__((deprecated))
#else
# define DEPRECATED__gui_interface__srv__Taskcmd_Request __declspec(deprecated)
#endif

namespace gui_interface
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Taskcmd_Request_
{
  using Type = Taskcmd_Request_<ContainerAllocator>;

  explicit Taskcmd_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->task = "";
    }
  }

  explicit Taskcmd_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : task(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->task = "";
    }
  }

  // field types and members
  using _task_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _task_type task;

  // setters for named parameter idiom
  Type & set__task(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->task = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    gui_interface::srv::Taskcmd_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const gui_interface::srv::Taskcmd_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      gui_interface::srv::Taskcmd_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      gui_interface::srv::Taskcmd_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__gui_interface__srv__Taskcmd_Request
    std::shared_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__gui_interface__srv__Taskcmd_Request
    std::shared_ptr<gui_interface::srv::Taskcmd_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Taskcmd_Request_ & other) const
  {
    if (this->task != other.task) {
      return false;
    }
    return true;
  }
  bool operator!=(const Taskcmd_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Taskcmd_Request_

// alias to use template instance with default allocator
using Taskcmd_Request =
  gui_interface::srv::Taskcmd_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace gui_interface


#ifndef _WIN32
# define DEPRECATED__gui_interface__srv__Taskcmd_Response __attribute__((deprecated))
#else
# define DEPRECATED__gui_interface__srv__Taskcmd_Response __declspec(deprecated)
#endif

namespace gui_interface
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct Taskcmd_Response_
{
  using Type = Taskcmd_Response_<ContainerAllocator>;

  explicit Taskcmd_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->state = 0ll;
    }
  }

  explicit Taskcmd_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
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
    gui_interface::srv::Taskcmd_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const gui_interface::srv::Taskcmd_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      gui_interface::srv::Taskcmd_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      gui_interface::srv::Taskcmd_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__gui_interface__srv__Taskcmd_Response
    std::shared_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__gui_interface__srv__Taskcmd_Response
    std::shared_ptr<gui_interface::srv::Taskcmd_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Taskcmd_Response_ & other) const
  {
    if (this->state != other.state) {
      return false;
    }
    return true;
  }
  bool operator!=(const Taskcmd_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Taskcmd_Response_

// alias to use template instance with default allocator
using Taskcmd_Response =
  gui_interface::srv::Taskcmd_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace gui_interface

namespace gui_interface
{

namespace srv
{

struct Taskcmd
{
  using Request = gui_interface::srv::Taskcmd_Request;
  using Response = gui_interface::srv::Taskcmd_Response;
};

}  // namespace srv

}  // namespace gui_interface

#endif  // GUI_INTERFACE__SRV__DETAIL__TASKCMD__STRUCT_HPP_
