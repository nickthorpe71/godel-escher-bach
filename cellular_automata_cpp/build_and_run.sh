#!/bin/bash

# Create a build directory if it doesn't exist
mkdir -p build
cd build

# Clean previous CMake cache
rm -rf *

# Run CMake to configure the project
cmake ..

# Build the project
make

# Run the executable
./GameOfLife