// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pallet_interfaces:msg/Boxinfo.idl
// generated code does not contain a copyright notice
#include "pallet_interfaces/msg/detail/boxinfo__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
pallet_interfaces__msg__Boxinfo__init(pallet_interfaces__msg__Boxinfo * msg)
{
  if (!msg) {
    return false;
  }
  // length
  // width
  // height
  return true;
}

void
pallet_interfaces__msg__Boxinfo__fini(pallet_interfaces__msg__Boxinfo * msg)
{
  if (!msg) {
    return;
  }
  // length
  // width
  // height
}

bool
pallet_interfaces__msg__Boxinfo__are_equal(const pallet_interfaces__msg__Boxinfo * lhs, const pallet_interfaces__msg__Boxinfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // length
  if (lhs->length != rhs->length) {
    return false;
  }
  // width
  if (lhs->width != rhs->width) {
    return false;
  }
  // height
  if (lhs->height != rhs->height) {
    return false;
  }
  return true;
}

bool
pallet_interfaces__msg__Boxinfo__copy(
  const pallet_interfaces__msg__Boxinfo * input,
  pallet_interfaces__msg__Boxinfo * output)
{
  if (!input || !output) {
    return false;
  }
  // length
  output->length = input->length;
  // width
  output->width = input->width;
  // height
  output->height = input->height;
  return true;
}

pallet_interfaces__msg__Boxinfo *
pallet_interfaces__msg__Boxinfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__msg__Boxinfo * msg = (pallet_interfaces__msg__Boxinfo *)allocator.allocate(sizeof(pallet_interfaces__msg__Boxinfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pallet_interfaces__msg__Boxinfo));
  bool success = pallet_interfaces__msg__Boxinfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pallet_interfaces__msg__Boxinfo__destroy(pallet_interfaces__msg__Boxinfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pallet_interfaces__msg__Boxinfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pallet_interfaces__msg__Boxinfo__Sequence__init(pallet_interfaces__msg__Boxinfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__msg__Boxinfo * data = NULL;

  if (size) {
    data = (pallet_interfaces__msg__Boxinfo *)allocator.zero_allocate(size, sizeof(pallet_interfaces__msg__Boxinfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pallet_interfaces__msg__Boxinfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pallet_interfaces__msg__Boxinfo__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
pallet_interfaces__msg__Boxinfo__Sequence__fini(pallet_interfaces__msg__Boxinfo__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      pallet_interfaces__msg__Boxinfo__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

pallet_interfaces__msg__Boxinfo__Sequence *
pallet_interfaces__msg__Boxinfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__msg__Boxinfo__Sequence * array = (pallet_interfaces__msg__Boxinfo__Sequence *)allocator.allocate(sizeof(pallet_interfaces__msg__Boxinfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pallet_interfaces__msg__Boxinfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pallet_interfaces__msg__Boxinfo__Sequence__destroy(pallet_interfaces__msg__Boxinfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pallet_interfaces__msg__Boxinfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pallet_interfaces__msg__Boxinfo__Sequence__are_equal(const pallet_interfaces__msg__Boxinfo__Sequence * lhs, const pallet_interfaces__msg__Boxinfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pallet_interfaces__msg__Boxinfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pallet_interfaces__msg__Boxinfo__Sequence__copy(
  const pallet_interfaces__msg__Boxinfo__Sequence * input,
  pallet_interfaces__msg__Boxinfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pallet_interfaces__msg__Boxinfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pallet_interfaces__msg__Boxinfo * data =
      (pallet_interfaces__msg__Boxinfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pallet_interfaces__msg__Boxinfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pallet_interfaces__msg__Boxinfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pallet_interfaces__msg__Boxinfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
