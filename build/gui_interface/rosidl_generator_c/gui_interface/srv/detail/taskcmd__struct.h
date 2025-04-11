// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from gui_interface:srv/Taskcmd.idl
// generated code does not contain a copyright notice

#ifndef GUI_INTERFACE__SRV__DETAIL__TASKCMD__STRUCT_H_
#define GUI_INTERFACE__SRV__DETAIL__TASKCMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'task'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/Taskcmd in the package gui_interface.
typedef struct gui_interface__srv__Taskcmd_Request
{
  rosidl_runtime_c__String task;
} gui_interface__srv__Taskcmd_Request;

// Struct for a sequence of gui_interface__srv__Taskcmd_Request.
typedef struct gui_interface__srv__Taskcmd_Request__Sequence
{
  gui_interface__srv__Taskcmd_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gui_interface__srv__Taskcmd_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/Taskcmd in the package gui_interface.
typedef struct gui_interface__srv__Taskcmd_Response
{
  int64_t state;
} gui_interface__srv__Taskcmd_Response;

// Struct for a sequence of gui_interface__srv__Taskcmd_Response.
typedef struct gui_interface__srv__Taskcmd_Response__Sequence
{
  gui_interface__srv__Taskcmd_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} gui_interface__srv__Taskcmd_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // GUI_INTERFACE__SRV__DETAIL__TASKCMD__STRUCT_H_
