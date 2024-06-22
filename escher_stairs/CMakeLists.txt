cmake_minimum_required(VERSION 3.10)
project(Escher3DStairs)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the executable
add_executable(escher_stairs src/main.cpp)

# Find OpenGL
find_package(OpenGL REQUIRED)

# Manually specify the paths for GLEW
set(GLEW_INCLUDE_DIRS "/usr/local/include")
set(GLEW_LIBRARIES "/usr/local/lib/libGLEW.dylib")

# Find GLFW
find_package(glfw3 3.3 REQUIRED)

# Include directories
include_directories(${OPENGL_INCLUDE_DIRS} ${GLEW_INCLUDE_DIRS} ${GLFW_INCLUDE_DIRS})

# Link libraries
target_link_libraries(escher_stairs ${OPENGL_LIBRARIES} ${GLEW_LIBRARIES} glfw)