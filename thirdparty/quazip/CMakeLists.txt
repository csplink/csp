set(name QuaZip)

file(GLOB_RECURSE SOURCES
        quazip/*.h
        quazip/*.cpp
        quazip/*.c
)

set(BUILD_SHARED_LIBS ON)

if (CMAKE_SYSTEM_NAME MATCHES "Windows")
    find_package(Qt5 REQUIRED COMPONENTS Zlib)
    set(ZLIB_LIBRARY Qt5::Zlib)
else ()
    find_package(ZLIB REQUIRED)
    set(ZLIB_LIBRARY ZLIB::ZLIB)
endif ()

add_library(${name} ${SOURCES})
target_link_libraries(${name} PUBLIC Qt5::Core ${ZLIB_LIBRARY})
target_include_directories(${name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/quazip)

if(BUILD_SHARED_LIBS)
	target_compile_definitions(${name} PRIVATE QUAZIP_BUILD) # dllexport
else()
	target_compile_definitions(${name} PUBLIC QUAZIP_STATIC) # suppress dllimport
endif()
