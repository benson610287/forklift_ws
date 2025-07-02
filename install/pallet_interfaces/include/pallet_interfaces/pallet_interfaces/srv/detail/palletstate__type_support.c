// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from pallet_interfaces:srv/Palletstate.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "pallet_interfaces/srv/detail/palletstate__rosidl_typesupport_introspection_c.h"
#include "pallet_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "pallet_interfaces/srv/detail/palletstate__functions.h"
#include "pallet_interfaces/srv/detail/palletstate__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pallet_interfaces__srv__Palletstate_Request__init(message_memory);
}

void pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_fini_function(void * message_memory)
{
  pallet_interfaces__srv__Palletstate_Request__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_member_array[1] = {
  {
    "run",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pallet_interfaces__srv__Palletstate_Request, run),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_members = {
  "pallet_interfaces__srv",  // message namespace
  "Palletstate_Request",  // message name
  1,  // number of fields
  sizeof(pallet_interfaces__srv__Palletstate_Request),
  pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_member_array,  // message members
  pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_init_function,  // function to initialize message memory (memory has to be allocated)
  pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_type_support_handle = {
  0,
  &pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pallet_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate_Request)() {
  if (!pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_type_support_handle.typesupport_identifier) {
    pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pallet_interfaces__srv__Palletstate_Request__rosidl_typesupport_introspection_c__Palletstate_Request_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

// already included above
// #include <stddef.h>
// already included above
// #include "pallet_interfaces/srv/detail/palletstate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "pallet_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "rosidl_typesupport_introspection_c/field_types.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
// already included above
// #include "rosidl_typesupport_introspection_c/message_introspection.h"
// already included above
// #include "pallet_interfaces/srv/detail/palletstate__functions.h"
// already included above
// #include "pallet_interfaces/srv/detail/palletstate__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  pallet_interfaces__srv__Palletstate_Response__init(message_memory);
}

void pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_fini_function(void * message_memory)
{
  pallet_interfaces__srv__Palletstate_Response__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_member_array[1] = {
  {
    "state",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(pallet_interfaces__srv__Palletstate_Response, state),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_members = {
  "pallet_interfaces__srv",  // message namespace
  "Palletstate_Response",  // message name
  1,  // number of fields
  sizeof(pallet_interfaces__srv__Palletstate_Response),
  pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_member_array,  // message members
  pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_init_function,  // function to initialize message memory (memory has to be allocated)
  pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_type_support_handle = {
  0,
  &pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pallet_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate_Response)() {
  if (!pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_type_support_handle.typesupport_identifier) {
    pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &pallet_interfaces__srv__Palletstate_Response__rosidl_typesupport_introspection_c__Palletstate_Response_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif

#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "pallet_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
// already included above
// #include "pallet_interfaces/srv/detail/palletstate__rosidl_typesupport_introspection_c.h"
// already included above
// #include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/service_introspection.h"

// this is intentionally not const to allow initialization later to prevent an initialization race
static rosidl_typesupport_introspection_c__ServiceMembers pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_members = {
  "pallet_interfaces__srv",  // service namespace
  "Palletstate",  // service name
  // these two fields are initialized below on the first access
  NULL,  // request message
  // pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_Request_message_type_support_handle,
  NULL  // response message
  // pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_Response_message_type_support_handle
};

static rosidl_service_type_support_t pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_type_support_handle = {
  0,
  &pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_members,
  get_service_typesupport_handle_function,
};

// Forward declaration of request/response type support functions
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate_Request)();

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate_Response)();

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_pallet_interfaces
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate)() {
  if (!pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_type_support_handle.typesupport_identifier) {
    pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  rosidl_typesupport_introspection_c__ServiceMembers * service_members =
    (rosidl_typesupport_introspection_c__ServiceMembers *)pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_type_support_handle.data;

  if (!service_members->request_members_) {
    service_members->request_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate_Request)()->data;
  }
  if (!service_members->response_members_) {
    service_members->response_members_ =
      (const rosidl_typesupport_introspection_c__MessageMembers *)
      ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, pallet_interfaces, srv, Palletstate_Response)()->data;
  }

  return &pallet_interfaces__srv__detail__palletstate__rosidl_typesupport_introspection_c__Palletstate_service_type_support_handle;
}
