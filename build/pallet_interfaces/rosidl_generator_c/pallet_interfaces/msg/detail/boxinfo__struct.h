// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from pallet_interfaces:msg/Boxinfo.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__MSG__DETAIL__BOXINFO__STRUCT_H_
#define PALLET_INTERFACES__MSG__DETAIL__BOXINFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Boxinfo in the package pallet_interfaces.
typedef struct pallet_interfaces__msg__Boxinfo
{
  double length;
  double width;
  double height;
} pallet_interfaces__msg__Boxinfo;

// Struct for a sequence of pallet_interfaces__msg__Boxinfo.
typedef struct pallet_interfaces__msg__Boxinfo__Sequence
{
  pallet_interfaces__msg__Boxinfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} pallet_interfaces__msg__Boxinfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // PALLET_INTERFACES__MSG__DETAIL__BOXINFO__STRUCT_H_
