cmake_minimum_required(VERSION 3.8)
project(mecanum)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()



# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
# find_package(libmodbus REQUIRED)
set(dependencies
  geometry_msgs
  # laser_geometry
  # map_msgs
  # message_filters
  # nav2_msgs
  # nav2_util
  # nav2_voxel_grid
  nav_msgs
  # pluginlib
  rclcpp
  # rclcpp_lifecycle
  # sensor_msgs
  # std_msgs
  # tf2
  # tf2_geometry_msgs
  tf2_ros
  tf2_geometry_msgs
  # tf2_sensor_msgs
  # visualization_msgs
  # angles  
)
include_directories(
  include
)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
# include_directories(${geometry_msgs_INCLUDE_DIRS})


add_executable(mobile_node src/mobile_node.cpp src/TimdaModbus.cpp src/Mecanum.cpp)
ament_target_dependencies(mobile_node ${dependencies}) 
target_link_libraries(mobile_node modbus)

# add_library(Mecanum src/Mecanum.cpp)
# add_library(TimdaModbus src/TimdaModbus.cpp)
# target_link_libraries(mobile_node Mecanum TimdaModbus)

install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION include/${PROJECT_NAME}
)

install(TARGETS
  mobile_node
  DESTINATION lib/${PROJECT_NAME}
)


if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
