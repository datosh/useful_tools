#!/usr/bin/env python3

import os
import subprocess
import shutil
import sys

folders_to_create = ["src", "include", "build", "test"]

# CMakeLists.txt for base directory
# We need to fill:
#   project_name
#   project_exe
#   project_test_exe
#   project_test_name
#
base_cmake_path = "CMakeLists.txt"
base_cmake = """cmake_minimum_required(VERSION 3.1.0 FATAL_ERROR)

# force clang
set(CMAKE_C_COMPILER clang)
set(CMAKE_CXX_COMPILER clang++)

project(##PROJECTNAME##)

# generate json-compilation-database
# this has to come after project(...) or else cmake .. has to be run twice
set(CMAKE_EXPORT_COMPILE_COMMANDS 1)

# Run clang format on all files
file(GLOB_RECURSE FILES_TO_FORMAT
    src/*
    include/*)
add_custom_target(format
    COMMAND clang-format
    -i
    ${FILES_TO_FORMAT})

# Run clang tidy on all files
file(GLOB_RECURSE FILES_TO_TIDY
    src/*
    include/*)
add_custom_target(tidy
    COMMAND clang-tidy
    -p ${CMAKE_BINARY_DIR}
    ${FILES_TO_TIDY})

# add compiler flags
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -std=c++1z")

# add includes
include_directories(${PROJECT_SOURCE_DIR}/include)

# Build daugther once so we can get all function needed in instrumentation
add_executable(##PROJECTNAME##
    ${PROJECT_SOURCE_DIR}/src/main.cpp)

add_subdirectory(test)
enable_testing()
add_test(NAME ##PROJECTNAME##_test COMMAND ##PROJECTNAME##_test)
"""

# CMakeLists.txt for test directory
# We need to fill:
#   project_test_exe
#   project_test_file
#
test_cmake_path = "test/CMakeLists.txt"
test_cmake = """find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

add_executable(##PROJECTNAME##_test
               ${CMAKE_CURRENT_LIST_DIR}/test.cpp)
target_link_libraries(##PROJECTNAME##_test
                      ${GTEST_BOTH_LIBRARIES}
                      pthread)
"""

# src/main.cpp
main_cpp_path = "src/main.cpp"
main_cpp = """#include <iostream>

int main(int argc, char **argv) {

    std::cout << "Hello: ##PROJECTNAME##\\n";
    return 0;
}

"""

# test/test.cpp
test_cpp_path = "test/test.cpp"
test_cpp = """#include "gtest/gtest.h"

TEST(##PROJECTNAME##Test, Positive) {
    EXPECT_EQ(1, 1);
}

TEST(##PROJECTNAME##Test, Negative) {
    EXPECT_NE(1, 2);
}

GTEST_API_ int main(int argc, char **argv) {
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
"""

files_to_create = [
    [base_cmake, base_cmake_path],
    [test_cmake, test_cmake_path],
    [main_cpp, main_cpp_path],
    [test_cpp, test_cpp_path],
]

files_to_copy = [
    (".clang-format", "."),
    (".clang-tidy", "."),
]


def checkUsage():
    if len(sys.argv) != 3:
        print("Usage: " + sys.argv[0] + " <path> <projectName>")
        sys.exit(-1)


def create_folders(project_path):
    for folder in folders_to_create:
        folder_path = os.path.join(project_path, folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)


def populate_names(project_name):
    placeholder = "##PROJECTNAME##"

    global files_to_create
    for i in range(len(files_to_create)):
        files_to_create[i][0] = files_to_create[i][0].replace(
            placeholder, project_name)


def create_files(project_path):
    for content, path in files_to_create:
        file_path = os.path.join(project_path, path)
        with open(file_path, 'w') as f:
            f.write(content)


def copy_files(project_path):
    exe_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    for src, dest in files_to_copy:
        dest_path = os.path.join(project_path, dest)
        src_path = os.path.join(exe_path, src)
        shutil.copy(src_path, dest_path)


def main():
    checkUsage()

    # Get project name
    project_name = sys.argv[2]

    # Work on absolute path to prevent any confusion
    path = os.path.abspath(sys.argv[1])
    print("Going to deplay project: '" + project_name + "' in: " + path)

    # Check and create root
    project_path = os.path.join(path, project_name)
    if not os.path.exists(project_path):
        os.mkdir(project_path)

    create_folders(project_path)
    populate_names(project_name)
    create_files(project_path)
    copy_files(project_path)

    # -a all so we see .clang-format etc
    subprocess.call(["tree", "-a", project_path])


if __name__ == '__main__':
    main()
