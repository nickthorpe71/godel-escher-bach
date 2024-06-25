cmake_minimum_required(VERSION 3.10)

# Set the project name and version
project(GameOfLife VERSION 1.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Add the executable
add_executable(GameOfLife src/main.cpp)

# Find SFML package
set(SFML_DIR "/usr/local/lib/cmake/SFML")
find_package(SFML 2.5 COMPONENTS graphics window system REQUIRED)

# Link SFML libraries
target_link_libraries(GameOfLife sfml-graphics sfml-window sfml-system)