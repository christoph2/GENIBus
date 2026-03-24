cmake_minimum_required(VERSION 3.20)

project(genibus_commlib LANGUAGES C CXX)

# Library currently contains C sources. Migration to full C++20 can be done
# incrementally by switching/adding translation units in later WPs.
set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(GENIBUS_BUILD_POSIX_SERIAL "Build POSIX serial backend" ON)
option(GENIBUS_BUILD_TESTS "Build commlib smoke tests" ON)

set(GENIBUS_COMMLIB_SOURCES
    src/crc.c
    src/datalink.c
)

if(GENIBUS_BUILD_POSIX_SERIAL AND UNIX)
    list(APPEND GENIBUS_COMMLIB_SOURCES src/posix_serial.c)
endif()

add_library(genibus_commlib STATIC ${GENIBUS_COMMLIB_SOURCES})

# Compile existing legacy .c translation units as C++20 to enable an
# incremental migration without large file moves in one step.
set_source_files_properties(${GENIBUS_COMMLIB_SOURCES} PROPERTIES LANGUAGE CXX)
target_compile_features(genibus_commlib PUBLIC cxx_std_20)

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

if(GENIBUS_BUILD_TESTS)
    include(CTest)
    if(BUILD_TESTING)
        add_executable(genibus_crc_smoke_test tests/smoke_crc.cpp)
        target_link_libraries(genibus_crc_smoke_test PRIVATE genibus_commlib)
        add_test(NAME genibus_crc_smoke_test COMMAND genibus_crc_smoke_test)

        add_executable(genibus_datalink_smoke_test tests/smoke_datalink.cpp)
        target_link_libraries(genibus_datalink_smoke_test PRIVATE genibus_commlib)
        add_test(NAME genibus_datalink_smoke_test COMMAND genibus_datalink_smoke_test)
    endif()
endif()

