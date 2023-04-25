cmake_minimum_required(VERSION 3.5)
project(small_robot_description)

# Default to C99
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 99)
endif()

# Default to C++14
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(urdf REQUIRED)

#=============
# Generate N urdf files, each with unique robot and frame names
# Source file is in ${CMAKE_CURRENT_SOURCE_DIR}/urdf/tello.xml
# Generated files are in ${CMAKE_CURRENT_BINARY_DIR}/urdf/telloX.urdf
#=============

file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/urdf")

foreach (INDEX RANGE 0 25)
  if (${INDEX} EQUAL 0)
    set(SUFFIX "00")
    set(TOPIC_NS "small_robot00")
  elseif (${INDEX} LESS 10)
    set(SUFFIX "0${INDEX}")
    set(TOPIC_NS "small_robot0${INDEX}")
  else ()
    set(SUFFIX "${INDEX}")
    set(TOPIC_NS "small_robot${INDEX}")
  endif ()
  set(URDF_FILE "${CMAKE_CURRENT_BINARY_DIR}/urdf/small_robot${SUFFIX}.urdf")
  message(STATUS "creating rules for ${URDF_FILE}")
  add_custom_command(
    OUTPUT ${URDF_FILE}
    COMMAND ${PYTHON_EXECUTABLE} "${CMAKE_CURRENT_SOURCE_DIR}/src/replace.py"
    "${CMAKE_CURRENT_SOURCE_DIR}/urdf/small_robot.xml" "suffix=${SUFFIX}" "topic_ns=${TOPIC_NS}" ">" "${URDF_FILE}"
    DEPENDS urdf/small_robot.xml
    COMMENT "Generate ${URDF_FILE}"
    VERBATIM
  )
  add_custom_target(generate_urdf${SUFFIX} ALL DEPENDS ${URDF_FILE})
endforeach ()

install(
  DIRECTORY
    meshes
    urdf
    launch
  DESTINATION
    share/${PROJECT_NAME}/
)

install(
  PROGRAMS
  src/replace.py # JLBC: Was "spawn_small_robot.py"
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
