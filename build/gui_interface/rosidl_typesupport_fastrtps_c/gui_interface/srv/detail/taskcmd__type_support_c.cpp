// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from gui_interface:srv/Taskcmd.idl
// generated code does not contain a copyright notice
#include "gui_interface/srv/detail/taskcmd__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "gui_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "gui_interface/srv/detail/taskcmd__struct.h"
#include "gui_interface/srv/detail/taskcmd__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // task
#include "rosidl_runtime_c/string_functions.h"  // task

// forward declare type support functions


using _Taskcmd_Request__ros_msg_type = gui_interface__srv__Taskcmd_Request;

static bool _Taskcmd_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Taskcmd_Request__ros_msg_type * ros_message = static_cast<const _Taskcmd_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: task
  {
    const rosidl_runtime_c__String * str = &ros_message->task;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _Taskcmd_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Taskcmd_Request__ros_msg_type * ros_message = static_cast<_Taskcmd_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: task
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->task.data) {
      rosidl_runtime_c__String__init(&ros_message->task);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->task,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'task'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_gui_interface
size_t get_serialized_size_gui_interface__srv__Taskcmd_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Taskcmd_Request__ros_msg_type * ros_message = static_cast<const _Taskcmd_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name task
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->task.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _Taskcmd_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_gui_interface__srv__Taskcmd_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_gui_interface
size_t max_serialized_size_gui_interface__srv__Taskcmd_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: task
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = gui_interface__srv__Taskcmd_Request;
    is_plain =
      (
      offsetof(DataType, task) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Taskcmd_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_gui_interface__srv__Taskcmd_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Taskcmd_Request = {
  "gui_interface::srv",
  "Taskcmd_Request",
  _Taskcmd_Request__cdr_serialize,
  _Taskcmd_Request__cdr_deserialize,
  _Taskcmd_Request__get_serialized_size,
  _Taskcmd_Request__max_serialized_size
};

static rosidl_message_type_support_t _Taskcmd_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Taskcmd_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, gui_interface, srv, Taskcmd_Request)() {
  return &_Taskcmd_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "gui_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "gui_interface/srv/detail/taskcmd__struct.h"
// already included above
// #include "gui_interface/srv/detail/taskcmd__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _Taskcmd_Response__ros_msg_type = gui_interface__srv__Taskcmd_Response;

static bool _Taskcmd_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Taskcmd_Response__ros_msg_type * ros_message = static_cast<const _Taskcmd_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: state
  {
    cdr << ros_message->state;
  }

  return true;
}

static bool _Taskcmd_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Taskcmd_Response__ros_msg_type * ros_message = static_cast<_Taskcmd_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: state
  {
    cdr >> ros_message->state;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_gui_interface
size_t get_serialized_size_gui_interface__srv__Taskcmd_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Taskcmd_Response__ros_msg_type * ros_message = static_cast<const _Taskcmd_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name state
  {
    size_t item_size = sizeof(ros_message->state);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Taskcmd_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_gui_interface__srv__Taskcmd_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_gui_interface
size_t max_serialized_size_gui_interface__srv__Taskcmd_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: state
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = gui_interface__srv__Taskcmd_Response;
    is_plain =
      (
      offsetof(DataType, state) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _Taskcmd_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_gui_interface__srv__Taskcmd_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_Taskcmd_Response = {
  "gui_interface::srv",
  "Taskcmd_Response",
  _Taskcmd_Response__cdr_serialize,
  _Taskcmd_Response__cdr_deserialize,
  _Taskcmd_Response__get_serialized_size,
  _Taskcmd_Response__max_serialized_size
};

static rosidl_message_type_support_t _Taskcmd_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Taskcmd_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, gui_interface, srv, Taskcmd_Response)() {
  return &_Taskcmd_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "gui_interface/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "gui_interface/srv/taskcmd.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t Taskcmd__callbacks = {
  "gui_interface::srv",
  "Taskcmd",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, gui_interface, srv, Taskcmd_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, gui_interface, srv, Taskcmd_Response)(),
};

static rosidl_service_type_support_t Taskcmd__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &Taskcmd__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, gui_interface, srv, Taskcmd)() {
  return &Taskcmd__handle;
}

#if defined(__cplusplus)
}
#endif
