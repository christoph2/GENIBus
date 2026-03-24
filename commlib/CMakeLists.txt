cmake_minimum_required(VERSION 3.20)

project(genibus_commlib LANGUAGES C)

# Library currently contains C sources. Migration to full C++20 can be done
# incrementally by switching/adding translation units in later WPs.
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

option(GENIBUS_BUILD_POSIX_SERIAL "Build POSIX serial backend" ON)

set(GENIBUS_COMMLIB_SOURCES
    src/crc.c
    src/datalink.c
)

if(GENIBUS_BUILD_POSIX_SERIAL AND UNIX)
    list(APPEND GENIBUS_COMMLIB_SOURCES src/posix_serial.c)
endif()

add_library(genibus_commlib STATIC ${GENIBUS_COMMLIB_SOURCES})

# Headers use includes like "genibus/types.h".
target_include_directories(genibus_commlib
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# Needed by posix_serial.h conditionals when POSIX backend is compiled.
if(GENIBUS_BUILD_POSIX_SERIAL AND UNIX)
    target_compile_definitions(genibus_commlib
        PUBLIC
            KNX_TARGET_POSIX=1
            KNX_TARGET_TYPE=1
    )
endif()

# Keep warnings practical for legacy code while still useful.
if(MSVC)
    target_compile_options(genibus_commlib PRIVATE /W3)
else()
    target_compile_options(genibus_commlib PRIVATE -Wall -Wextra)
endif()

