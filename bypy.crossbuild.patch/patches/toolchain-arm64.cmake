# 这里设置cmake支持的最小版本
cmake_minimum_required(VERSION 3.18)
include_guard(GLOBAL)

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

# 指定sysroot目录
set(TARGET_SYSROOT /opt/cross)
set(CMAKE_SYSROOT ${TARGET_SYSROOT})

# 指定交叉编译器路径
set(CROSS_COMPILER /opt/aarch64-linux-musl-cross/bin/aarch64-linux-musl)
set(CMAKE_C_COMPILER ${CROSS_COMPILER}-gcc)
set(CMAKE_CXX_COMPILER ${CROSS_COMPILER}-g++)

set(CMAKE_C_FLAGS "-I/sw/sw/include -I/opt/cross/usr/include")
set(CMAKE_CXX_FLAGS "-I/sw/sw/include -I/opt/cross/usr/include")

set(CMAKE_FIND_ROOT_PATH "/sw/sw;/opt/cross")

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

