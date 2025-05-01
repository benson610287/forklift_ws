// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from docking_interface:srv/Dockingstatus.idl
// generated code does not contain a copyright notice
#include "docking_interface/srv/detail/dockingstatus__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

bool
docking_interface__srv__Dockingstatus_Request__init(docking_interface__srv__Dockingstatus_Request * msg)
{
  if (!msg) {
    return false;
  }
  // run
  return true;
}

void
docking_interface__srv__Dockingstatus_Request__fini(docking_interface__srv__Dockingstatus_Request * msg)
{
  if (!msg) {
    return;
  }
  // run
}

bool
docking_interface__srv__Dockingstatus_Request__are_equal(const docking_interface__srv__Dockingstatus_Request * lhs, const docking_interface__srv__Dockingstatus_Request * rhs)
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
docking_interface__srv__Dockingstatus_Request__copy(
  const docking_interface__srv__Dockingstatus_Request * input,
  docking_interface__srv__Dockingstatus_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // run
  output->run = input->run;
  return true;
}

docking_interface__srv__Dockingstatus_Request *
docking_interface__srv__Dockingstatus_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  docking_interface__srv__Dockingstatus_Request * msg = (docking_interface__srv__Dockingstatus_Request *)allocator.allocate(sizeof(docking_interface__srv__Dockingstatus_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(docking_interface__srv__Dockingstatus_Request));
  bool success = docking_interface__srv__Dockingstatus_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
docking_interface__srv__Dockingstatus_Request__destroy(docking_interface__srv__Dockingstatus_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    docking_interface__srv__Dockingstatus_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
docking_interface__srv__Dockingstatus_Request__Sequence__init(docking_interface__srv__Dockingstatus_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  docking_interface__srv__Dockingstatus_Request * data = NULL;

  if (size) {
    data = (docking_interface__srv__Dockingstatus_Request *)allocator.zero_allocate(size, sizeof(docking_interface__srv__Dockingstatus_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = docking_interface__srv__Dockingstatus_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        docking_interface__srv__Dockingstatus_Request__fini(&data[i - 1]);
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
docking_interface__srv__Dockingstatus_Request__Sequence__fini(docking_interface__srv__Dockingstatus_Request__Sequence * array)
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
      docking_interface__srv__Dockingstatus_Request__fini(&array->data[i]);
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

docking_interface__srv__Dockingstatus_Request__Sequence *
docking_interface__srv__Dockingstatus_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  docking_interface__srv__Dockingstatus_Request__Sequence * array = (docking_interface__srv__Dockingstatus_Request__Sequence *)allocator.allocate(sizeof(docking_interface__srv__Dockingstatus_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = docking_interface__srv__Dockingstatus_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
docking_interface__srv__Dockingstatus_Request__Sequence__destroy(docking_interface__srv__Dockingstatus_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    docking_interface__srv__Dockingstatus_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
docking_interface__srv__Dockingstatus_Request__Sequence__are_equal(const docking_interface__srv__Dockingstatus_Request__Sequence * lhs, const docking_interface__srv__Dockingstatus_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!docking_interface__srv__Dockingstatus_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
docking_interface__srv__Dockingstatus_Request__Sequence__copy(
  const docking_interface__srv__Dockingstatus_Request__Sequence * input,
  docking_interface__srv__Dockingstatus_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(docking_interface__srv__Dockingstatus_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    docking_interface__srv__Dockingstatus_Request * data =
      (docking_interface__srv__Dockingstatus_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!docking_interface__srv__Dockingstatus_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          docking_interface__srv__Dockingstatus_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!docking_interface__srv__Dockingstatus_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
docking_interface__srv__Dockingstatus_Response__init(docking_interface__srv__Dockingstatus_Response * msg)
{
  if (!msg) {
    return false;
  }
  // state
  return true;
}

void
docking_interface__srv__Dockingstatus_Response__fini(docking_interface__srv__Dockingstatus_Response * msg)
{
  if (!msg) {
    return;
  }
  // state
}

bool
docking_interface__srv__Dockingstatus_Response__are_equal(const docking_interface__srv__Dockingstatus_Response * lhs, const docking_interface__srv__Dockingstatus_Response * rhs)
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
docking_interface__srv__Dockingstatus_Response__copy(
  const docking_interface__srv__Dockingstatus_Response * input,
  docking_interface__srv__Dockingstatus_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // state
  output->state = input->state;
  return true;
}

docking_interface__srv__Dockingstatus_Response *
docking_interface__srv__Dockingstatus_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  docking_interface__srv__Dockingstatus_Response * msg = (docking_interface__srv__Dockingstatus_Response *)allocator.allocate(sizeof(docking_interface__srv__Dockingstatus_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(docking_interface__srv__Dockingstatus_Response));
  bool success = docking_interface__srv__Dockingstatus_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
docking_interface__srv__Dockingstatus_Response__destroy(docking_interface__srv__Dockingstatus_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    docking_interface__srv__Dockingstatus_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
docking_interface__srv__Dockingstatus_Response__Sequence__init(docking_interface__srv__Dockingstatus_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  docking_interface__srv__Dockingstatus_Response * data = NULL;

  if (size) {
    data = (docking_interface__srv__Dockingstatus_Response *)allocator.zero_allocate(size, sizeof(docking_interface__srv__Dockingstatus_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = docking_interface__srv__Dockingstatus_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        docking_interface__srv__Dockingstatus_Response__fini(&data[i - 1]);
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
docking_interface__srv__Dockingstatus_Response__Sequence__fini(docking_interface__srv__Dockingstatus_Response__Sequence * array)
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
      docking_interface__srv__Dockingstatus_Response__fini(&array->data[i]);
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

docking_interface__srv__Dockingstatus_Response__Sequence *
docking_interface__srv__Dockingstatus_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  docking_interface__srv__Dockingstatus_Response__Sequence * array = (docking_interface__srv__Dockingstatus_Response__Sequence *)allocator.allocate(sizeof(docking_interface__srv__Dockingstatus_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = docking_interface__srv__Dockingstatus_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
docking_interface__srv__Dockingstatus_Response__Sequence__destroy(docking_interface__srv__Dockingstatus_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    docking_interface__srv__Dockingstatus_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
docking_interface__srv__Dockingstatus_Response__Sequence__are_equal(const docking_interface__srv__Dockingstatus_Response__Sequence * lhs, const docking_interface__srv__Dockingstatus_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!docking_interface__srv__Dockingstatus_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
docking_interface__srv__Dockingstatus_Response__Sequence__copy(
  const docking_interface__srv__Dockingstatus_Response__Sequence * input,
  docking_interface__srv__Dockingstatus_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(docking_interface__srv__Dockingstatus_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    docking_interface__srv__Dockingstatus_Response * data =
      (docking_interface__srv__Dockingstatus_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!docking_interface__srv__Dockingstatus_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          docking_interface__srv__Dockingstatus_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!docking_interface__srv__Dockingstatus_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
