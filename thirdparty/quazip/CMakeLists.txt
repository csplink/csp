set(name QuaZip)

file(GLOB_RECURSE HEADERS
        quazip/*.h
)

file(GLOB_RECURSE SOURCES
        quazip/*.h
        quazip/*.cpp
        quazip/*.c
)


set(BUILD_SHARED_LIBS ON)

add_library(${name} ${SOURCES})
target_link_libraries(${name} PUBLIC Qt5::Core)
target_include_directories(${name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/quazip)

if(BUILD_SHARED_LIBS)
	target_compile_definitions(${name} PRIVATE QUAZIP_BUILD) # dllexport
else()
	target_compile_definitions(${name} PUBLIC QUAZIP_STATIC) # suppress dllimport
endif()
