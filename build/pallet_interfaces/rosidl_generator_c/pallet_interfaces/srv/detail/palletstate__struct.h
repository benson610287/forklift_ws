// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pallet_interfaces:srv/Palletstate.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__STRUCT_H_
#define PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/Palletstate in the package pallet_interfaces.
typedef struct pallet_interfaces__srv__Palletstate_Request
{
  bool run;
} pallet_interfaces__srv__Palletstate_Request;

// Struct for a sequence of pallet_interfaces__srv__Palletstate_Request.
typedef struct pallet_interfaces__srv__Palletstate_Request__Sequence
{
  pallet_interfaces__srv__Palletstate_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pallet_interfaces__srv__Palletstate_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/Palletstate in the package pallet_interfaces.
typedef struct pallet_interfaces__srv__Palletstate_Response
{
  int64_t state;
} pallet_interfaces__srv__Palletstate_Response;

// Struct for a sequence of pallet_interfaces__srv__Palletstate_Response.
typedef struct pallet_interfaces__srv__Palletstate_Response__Sequence
{
  pallet_interfaces__srv__Palletstate_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pallet_interfaces__srv__Palletstate_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PALLET_INTERFACES__SRV__DETAIL__PALLETSTATE__STRUCT_H_
