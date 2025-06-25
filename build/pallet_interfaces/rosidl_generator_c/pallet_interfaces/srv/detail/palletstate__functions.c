// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from pallet_interfaces:srv/Palletstate.idl
// generated code does not contain a copyright notice
#include "pallet_interfaces/srv/detail/palletstate__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
pallet_interfaces__srv__Palletstate_Request__init(pallet_interfaces__srv__Palletstate_Request * msg)
{
  if (!msg) {
    return false;
  }
  // run
  return true;
}

void
pallet_interfaces__srv__Palletstate_Request__fini(pallet_interfaces__srv__Palletstate_Request * msg)
{
  if (!msg) {
    return;
  }
  // run
}

bool
pallet_interfaces__srv__Palletstate_Request__are_equal(const pallet_interfaces__srv__Palletstate_Request * lhs, const pallet_interfaces__srv__Palletstate_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // run
  if (lhs->run != rhs->run) {
    return false;
  }
  return true;
}

bool
pallet_interfaces__srv__Palletstate_Request__copy(
  const pallet_interfaces__srv__Palletstate_Request * input,
  pallet_interfaces__srv__Palletstate_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // run
  output->run = input->run;
  return true;
}

pallet_interfaces__srv__Palletstate_Request *
pallet_interfaces__srv__Palletstate_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__srv__Palletstate_Request * msg = (pallet_interfaces__srv__Palletstate_Request *)allocator.allocate(sizeof(pallet_interfaces__srv__Palletstate_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pallet_interfaces__srv__Palletstate_Request));
  bool success = pallet_interfaces__srv__Palletstate_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pallet_interfaces__srv__Palletstate_Request__destroy(pallet_interfaces__srv__Palletstate_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pallet_interfaces__srv__Palletstate_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pallet_interfaces__srv__Palletstate_Request__Sequence__init(pallet_interfaces__srv__Palletstate_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__srv__Palletstate_Request * data = NULL;

  if (size) {
    data = (pallet_interfaces__srv__Palletstate_Request *)allocator.zero_allocate(size, sizeof(pallet_interfaces__srv__Palletstate_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pallet_interfaces__srv__Palletstate_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pallet_interfaces__srv__Palletstate_Request__fini(&data[i - 1]);
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
pallet_interfaces__srv__Palletstate_Request__Sequence__fini(pallet_interfaces__srv__Palletstate_Request__Sequence * array)
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
      pallet_interfaces__srv__Palletstate_Request__fini(&array->data[i]);
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

pallet_interfaces__srv__Palletstate_Request__Sequence *
pallet_interfaces__srv__Palletstate_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__srv__Palletstate_Request__Sequence * array = (pallet_interfaces__srv__Palletstate_Request__Sequence *)allocator.allocate(sizeof(pallet_interfaces__srv__Palletstate_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pallet_interfaces__srv__Palletstate_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pallet_interfaces__srv__Palletstate_Request__Sequence__destroy(pallet_interfaces__srv__Palletstate_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pallet_interfaces__srv__Palletstate_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pallet_interfaces__srv__Palletstate_Request__Sequence__are_equal(const pallet_interfaces__srv__Palletstate_Request__Sequence * lhs, const pallet_interfaces__srv__Palletstate_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pallet_interfaces__srv__Palletstate_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pallet_interfaces__srv__Palletstate_Request__Sequence__copy(
  const pallet_interfaces__srv__Palletstate_Request__Sequence * input,
  pallet_interfaces__srv__Palletstate_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pallet_interfaces__srv__Palletstate_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pallet_interfaces__srv__Palletstate_Request * data =
      (pallet_interfaces__srv__Palletstate_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pallet_interfaces__srv__Palletstate_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pallet_interfaces__srv__Palletstate_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pallet_interfaces__srv__Palletstate_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
pallet_interfaces__srv__Palletstate_Response__init(pallet_interfaces__srv__Palletstate_Response * msg)
{
  if (!msg) {
    return false;
  }
  // state
  return true;
}

void
pallet_interfaces__srv__Palletstate_Response__fini(pallet_interfaces__srv__Palletstate_Response * msg)
{
  if (!msg) {
    return;
  }
  // state
}

bool
pallet_interfaces__srv__Palletstate_Response__are_equal(const pallet_interfaces__srv__Palletstate_Response * lhs, const pallet_interfaces__srv__Palletstate_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // state
  if (lhs->state != rhs->state) {
    return false;
  }
  return true;
}

bool
pallet_interfaces__srv__Palletstate_Response__copy(
  const pallet_interfaces__srv__Palletstate_Response * input,
  pallet_interfaces__srv__Palletstate_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // state
  output->state = input->state;
  return true;
}

pallet_interfaces__srv__Palletstate_Response *
pallet_interfaces__srv__Palletstate_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__srv__Palletstate_Response * msg = (pallet_interfaces__srv__Palletstate_Response *)allocator.allocate(sizeof(pallet_interfaces__srv__Palletstate_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(pallet_interfaces__srv__Palletstate_Response));
  bool success = pallet_interfaces__srv__Palletstate_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
pallet_interfaces__srv__Palletstate_Response__destroy(pallet_interfaces__srv__Palletstate_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    pallet_interfaces__srv__Palletstate_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
pallet_interfaces__srv__Palletstate_Response__Sequence__init(pallet_interfaces__srv__Palletstate_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__srv__Palletstate_Response * data = NULL;

  if (size) {
    data = (pallet_interfaces__srv__Palletstate_Response *)allocator.zero_allocate(size, sizeof(pallet_interfaces__srv__Palletstate_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = pallet_interfaces__srv__Palletstate_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        pallet_interfaces__srv__Palletstate_Response__fini(&data[i - 1]);
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
pallet_interfaces__srv__Palletstate_Response__Sequence__fini(pallet_interfaces__srv__Palletstate_Response__Sequence * array)
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
      pallet_interfaces__srv__Palletstate_Response__fini(&array->data[i]);
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

pallet_interfaces__srv__Palletstate_Response__Sequence *
pallet_interfaces__srv__Palletstate_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  pallet_interfaces__srv__Palletstate_Response__Sequence * array = (pallet_interfaces__srv__Palletstate_Response__Sequence *)allocator.allocate(sizeof(pallet_interfaces__srv__Palletstate_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = pallet_interfaces__srv__Palletstate_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
pallet_interfaces__srv__Palletstate_Response__Sequence__destroy(pallet_interfaces__srv__Palletstate_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    pallet_interfaces__srv__Palletstate_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
pallet_interfaces__srv__Palletstate_Response__Sequence__are_equal(const pallet_interfaces__srv__Palletstate_Response__Sequence * lhs, const pallet_interfaces__srv__Palletstate_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!pallet_interfaces__srv__Palletstate_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
pallet_interfaces__srv__Palletstate_Response__Sequence__copy(
  const pallet_interfaces__srv__Palletstate_Response__Sequence * input,
  pallet_interfaces__srv__Palletstate_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(pallet_interfaces__srv__Palletstate_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    pallet_interfaces__srv__Palletstate_Response * data =
      (pallet_interfaces__srv__Palletstate_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!pallet_interfaces__srv__Palletstate_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          pallet_interfaces__srv__Palletstate_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!pallet_interfaces__srv__Palletstate_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
