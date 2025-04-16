// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from pallet_interfaces:msg/Boxinfo.idl
// generated code does not contain a copyright notice

#ifndef PALLET_INTERFACES__MSG__DETAIL__BOXINFO__FUNCTIONS_H_
#define PALLET_INTERFACES__MSG__DETAIL__BOXINFO__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "pallet_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "pallet_interfaces/msg/detail/boxinfo__struct.h"

/// Initialize msg/Boxinfo message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * pallet_interfaces__msg__Boxinfo
 * )) before or use
 * pallet_interfaces__msg__Boxinfo__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
bool
pallet_interfaces__msg__Boxinfo__init(pallet_interfaces__msg__Boxinfo * msg);

/// Finalize msg/Boxinfo message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
void
pallet_interfaces__msg__Boxinfo__fini(pallet_interfaces__msg__Boxinfo * msg);

/// Create msg/Boxinfo message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * pallet_interfaces__msg__Boxinfo__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
pallet_interfaces__msg__Boxinfo *
pallet_interfaces__msg__Boxinfo__create();

/// Destroy msg/Boxinfo message.
/**
 * It calls
 * pallet_interfaces__msg__Boxinfo__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
void
pallet_interfaces__msg__Boxinfo__destroy(pallet_interfaces__msg__Boxinfo * msg);

/// Check for msg/Boxinfo message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
bool
pallet_interfaces__msg__Boxinfo__are_equal(const pallet_interfaces__msg__Boxinfo * lhs, const pallet_interfaces__msg__Boxinfo * rhs);

/// Copy a msg/Boxinfo message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
bool
pallet_interfaces__msg__Boxinfo__copy(
  const pallet_interfaces__msg__Boxinfo * input,
  pallet_interfaces__msg__Boxinfo * output);

/// Initialize array of msg/Boxinfo messages.
/**
 * It allocates the memory for the number of elements and calls
 * pallet_interfaces__msg__Boxinfo__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
bool
pallet_interfaces__msg__Boxinfo__Sequence__init(pallet_interfaces__msg__Boxinfo__Sequence * array, size_t size);

/// Finalize array of msg/Boxinfo messages.
/**
 * It calls
 * pallet_interfaces__msg__Boxinfo__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
void
pallet_interfaces__msg__Boxinfo__Sequence__fini(pallet_interfaces__msg__Boxinfo__Sequence * array);

/// Create array of msg/Boxinfo messages.
/**
 * It allocates the memory for the array and calls
 * pallet_interfaces__msg__Boxinfo__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
pallet_interfaces__msg__Boxinfo__Sequence *
pallet_interfaces__msg__Boxinfo__Sequence__create(size_t size);

/// Destroy array of msg/Boxinfo messages.
/**
 * It calls
 * pallet_interfaces__msg__Boxinfo__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
void
pallet_interfaces__msg__Boxinfo__Sequence__destroy(pallet_interfaces__msg__Boxinfo__Sequence * array);

/// Check for msg/Boxinfo message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
bool
pallet_interfaces__msg__Boxinfo__Sequence__are_equal(const pallet_interfaces__msg__Boxinfo__Sequence * lhs, const pallet_interfaces__msg__Boxinfo__Sequence * rhs);

/// Copy an array of msg/Boxinfo messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_pallet_interfaces
bool
pallet_interfaces__msg__Boxinfo__Sequence__copy(
  const pallet_interfaces__msg__Boxinfo__Sequence * input,
  pallet_interfaces__msg__Boxinfo__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // PALLET_INTERFACES__MSG__DETAIL__BOXINFO__FUNCTIONS_H_
