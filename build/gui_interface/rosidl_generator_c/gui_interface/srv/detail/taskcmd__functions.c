// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from gui_interface:srv/Taskcmd.idl
// generated code does not contain a copyright notice
#include "gui_interface/srv/detail/taskcmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `task`
#include "rosidl_runtime_c/string_functions.h"

bool
gui_interface__srv__Taskcmd_Request__init(gui_interface__srv__Taskcmd_Request * msg)
{
  if (!msg) {
    return false;
  }
  // task
  if (!rosidl_runtime_c__String__init(&msg->task)) {
    gui_interface__srv__Taskcmd_Request__fini(msg);
    return false;
  }
  return true;
}

void
gui_interface__srv__Taskcmd_Request__fini(gui_interface__srv__Taskcmd_Request * msg)
{
  if (!msg) {
    return;
  }
  // task
  rosidl_runtime_c__String__fini(&msg->task);
}

bool
gui_interface__srv__Taskcmd_Request__are_equal(const gui_interface__srv__Taskcmd_Request * lhs, const gui_interface__srv__Taskcmd_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // task
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->task), &(rhs->task)))
  {
    return false;
  }
  return true;
}

bool
gui_interface__srv__Taskcmd_Request__copy(
  const gui_interface__srv__Taskcmd_Request * input,
  gui_interface__srv__Taskcmd_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // task
  if (!rosidl_runtime_c__String__copy(
      &(input->task), &(output->task)))
  {
    return false;
  }
  return true;
}

gui_interface__srv__Taskcmd_Request *
gui_interface__srv__Taskcmd_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gui_interface__srv__Taskcmd_Request * msg = (gui_interface__srv__Taskcmd_Request *)allocator.allocate(sizeof(gui_interface__srv__Taskcmd_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gui_interface__srv__Taskcmd_Request));
  bool success = gui_interface__srv__Taskcmd_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gui_interface__srv__Taskcmd_Request__destroy(gui_interface__srv__Taskcmd_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gui_interface__srv__Taskcmd_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gui_interface__srv__Taskcmd_Request__Sequence__init(gui_interface__srv__Taskcmd_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gui_interface__srv__Taskcmd_Request * data = NULL;

  if (size) {
    data = (gui_interface__srv__Taskcmd_Request *)allocator.zero_allocate(size, sizeof(gui_interface__srv__Taskcmd_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gui_interface__srv__Taskcmd_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gui_interface__srv__Taskcmd_Request__fini(&data[i - 1]);
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
gui_interface__srv__Taskcmd_Request__Sequence__fini(gui_interface__srv__Taskcmd_Request__Sequence * array)
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
      gui_interface__srv__Taskcmd_Request__fini(&array->data[i]);
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

gui_interface__srv__Taskcmd_Request__Sequence *
gui_interface__srv__Taskcmd_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gui_interface__srv__Taskcmd_Request__Sequence * array = (gui_interface__srv__Taskcmd_Request__Sequence *)allocator.allocate(sizeof(gui_interface__srv__Taskcmd_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gui_interface__srv__Taskcmd_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gui_interface__srv__Taskcmd_Request__Sequence__destroy(gui_interface__srv__Taskcmd_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gui_interface__srv__Taskcmd_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gui_interface__srv__Taskcmd_Request__Sequence__are_equal(const gui_interface__srv__Taskcmd_Request__Sequence * lhs, const gui_interface__srv__Taskcmd_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gui_interface__srv__Taskcmd_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gui_interface__srv__Taskcmd_Request__Sequence__copy(
  const gui_interface__srv__Taskcmd_Request__Sequence * input,
  gui_interface__srv__Taskcmd_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gui_interface__srv__Taskcmd_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gui_interface__srv__Taskcmd_Request * data =
      (gui_interface__srv__Taskcmd_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gui_interface__srv__Taskcmd_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gui_interface__srv__Taskcmd_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gui_interface__srv__Taskcmd_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


bool
gui_interface__srv__Taskcmd_Response__init(gui_interface__srv__Taskcmd_Response * msg)
{
  if (!msg) {
    return false;
  }
  // state
  return true;
}

void
gui_interface__srv__Taskcmd_Response__fini(gui_interface__srv__Taskcmd_Response * msg)
{
  if (!msg) {
    return;
  }
  // state
}

bool
gui_interface__srv__Taskcmd_Response__are_equal(const gui_interface__srv__Taskcmd_Response * lhs, const gui_interface__srv__Taskcmd_Response * rhs)
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
gui_interface__srv__Taskcmd_Response__copy(
  const gui_interface__srv__Taskcmd_Response * input,
  gui_interface__srv__Taskcmd_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // state
  output->state = input->state;
  return true;
}

gui_interface__srv__Taskcmd_Response *
gui_interface__srv__Taskcmd_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gui_interface__srv__Taskcmd_Response * msg = (gui_interface__srv__Taskcmd_Response *)allocator.allocate(sizeof(gui_interface__srv__Taskcmd_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(gui_interface__srv__Taskcmd_Response));
  bool success = gui_interface__srv__Taskcmd_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
gui_interface__srv__Taskcmd_Response__destroy(gui_interface__srv__Taskcmd_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    gui_interface__srv__Taskcmd_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
gui_interface__srv__Taskcmd_Response__Sequence__init(gui_interface__srv__Taskcmd_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gui_interface__srv__Taskcmd_Response * data = NULL;

  if (size) {
    data = (gui_interface__srv__Taskcmd_Response *)allocator.zero_allocate(size, sizeof(gui_interface__srv__Taskcmd_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = gui_interface__srv__Taskcmd_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        gui_interface__srv__Taskcmd_Response__fini(&data[i - 1]);
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
gui_interface__srv__Taskcmd_Response__Sequence__fini(gui_interface__srv__Taskcmd_Response__Sequence * array)
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
      gui_interface__srv__Taskcmd_Response__fini(&array->data[i]);
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

gui_interface__srv__Taskcmd_Response__Sequence *
gui_interface__srv__Taskcmd_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  gui_interface__srv__Taskcmd_Response__Sequence * array = (gui_interface__srv__Taskcmd_Response__Sequence *)allocator.allocate(sizeof(gui_interface__srv__Taskcmd_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = gui_interface__srv__Taskcmd_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
gui_interface__srv__Taskcmd_Response__Sequence__destroy(gui_interface__srv__Taskcmd_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    gui_interface__srv__Taskcmd_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
gui_interface__srv__Taskcmd_Response__Sequence__are_equal(const gui_interface__srv__Taskcmd_Response__Sequence * lhs, const gui_interface__srv__Taskcmd_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!gui_interface__srv__Taskcmd_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
gui_interface__srv__Taskcmd_Response__Sequence__copy(
  const gui_interface__srv__Taskcmd_Response__Sequence * input,
  gui_interface__srv__Taskcmd_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(gui_interface__srv__Taskcmd_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    gui_interface__srv__Taskcmd_Response * data =
      (gui_interface__srv__Taskcmd_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!gui_interface__srv__Taskcmd_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          gui_interface__srv__Taskcmd_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!gui_interface__srv__Taskcmd_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
