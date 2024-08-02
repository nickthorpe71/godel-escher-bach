#!/bin/bash

# Create a build directory if it doesn't exist
mkdir -p build
cd build

# Clean previous CMake cache
rm -rf *

# Run CMake to configure the project for cross-compilation
cmake .. -DCMAKE_TOOLCHAIN_FILE=../toolchain-mingw32.cmake

# Build the project
make

# Notify user of the successful build
echo "Build completed. The Windows executable is located in the build directory."