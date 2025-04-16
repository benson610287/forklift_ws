// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from docking_interface:srv/Dockingstatus.idl
// generated code does not contain a copyright notice

#ifndef DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__STRUCT_H_
#define DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/Dockingstatus in the package docking_interface.
typedef struct docking_interface__srv__Dockingstatus_Request
{
  bool run;
} docking_interface__srv__Dockingstatus_Request;

// Struct for a sequence of docking_interface__srv__Dockingstatus_Request.
typedef struct docking_interface__srv__Dockingstatus_Request__Sequence
{
  docking_interface__srv__Dockingstatus_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} docking_interface__srv__Dockingstatus_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/Dockingstatus in the package docking_interface.
typedef struct docking_interface__srv__Dockingstatus_Response
{
  int64_t state;
} docking_interface__srv__Dockingstatus_Response;

// Struct for a sequence of docking_interface__srv__Dockingstatus_Response.
typedef struct docking_interface__srv__Dockingstatus_Response__Sequence
{
  docking_interface__srv__Dockingstatus_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} docking_interface__srv__Dockingstatus_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // DOCKING_INTERFACE__SRV__DETAIL__DOCKINGSTATUS__STRUCT_H_
