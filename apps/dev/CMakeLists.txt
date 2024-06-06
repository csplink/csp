#
# Licensed under the GNU General Public License v. 3 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        CMakeLists.txt
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-04-18     xqyjlj       initial version
#

set(name csp-dev)

set(CSP_EXE_DIR ${CMAKE_CURRENT_BINARY_DIR} CACHE INTERNAL "csp exe file dir")

configure_file(
        ${CMAKE_CURRENT_SOURCE_DIR}/Configure.h.in
        ${CMAKE_CURRENT_SOURCE_DIR}/Configure.h
)

file(GLOB COMPONENTS
        components/jobs/*.cpp components/jobs/*.h
        components/misc/*.cpp components/misc/*.h
        components/package/*.cpp components/package/*.h
        components/parse/*.cpp components/parse/*.h
        components/project/*.cpp components/project/*.h
        components/repo/*.cpp components/repo/*.h
        components/settings/*.cpp components/settings/*.h
        components/tools/*.cpp components/tools/*.h)

file(GLOB WIDGETS
        widgets/*.h widgets/*.cpp
        widgets/interface/*.h
        widgets/packages/*.h widgets/packages/*.cpp)

file(GLOB RESOURCES
        resources/*.qrc resources/*.rc
        ${CMAKE_CURRENT_SOURCE_DIR}/../../resources/icons/resources.qrc)

file(GLOB VIEWS
        views/*.ui views/*.h views/*.cpp
        views/dialogs/*.ui views/dialogs/*.h views/dialogs/*.cpp
        views/docks/*.ui views/docks/*.h views/docks/*.cpp)

set(TS_FILES
        ./resources/translations/${name}.zh_CN.ts
        ./resources/translations/${name}.zh_TW.ts)

set(PROJECT_SOURCES Main.cpp ${COMPONENTS} ${WIDGETS} ${RESOURCES} ${VIEWS} ${TS_FILES})

include_directories(
        .
        views views/dialogs views/docks
        widgets widgets/packages widgets/interface
        components/jobs components/misc components/package components/parse
        components/project components/repo components/settings
        components/tools)

foreach (TS_FILE ${TS_FILES})
    set_source_files_properties(${TS_FILE} PROPERTIES OUTPUT_LOCATION
            ${CMAKE_CURRENT_BINARY_DIR}/translations)
endforeach ()

qt5_create_translation(QM_FILES ${PROJECT_SOURCES} ${TS_FILES})

if (${CMAKE_BUILD_TYPE} MATCHES "Release")
    add_executable(${name} WIN32 ${PROJECT_SOURCES} ${QM_FILES})
else ()
    add_executable(${name} ${PROJECT_SOURCES} ${QM_FILES})
endif ()

set(DEPS custom_res custom_tools)
set(LIBS Qt5::Widgets Qt5::OpenGL qtpropertybrowser nlohmann-json yaml-cpp QuaZip)

add_dependencies(${name} ${DEPS})

target_link_libraries(${name} PRIVATE ${LIBS})

##########################################################################

set(name_package_installer "csp-package-installer")
set(PROJECT_SOURCES tools/package-installer/Main.cpp ${COMPONENTS} ${WIDGETS} ${RESOURCES} ${VIEWS})
if (${CMAKE_BUILD_TYPE} MATCHES "Release")
    add_executable(${name_package_installer} WIN32 ${PROJECT_SOURCES})
else ()
    add_executable(${name_package_installer} ${PROJECT_SOURCES})
endif ()
target_link_libraries(${name_package_installer} PRIVATE ${LIBS})

##########################################################################

set(name_test "${name}-test")
set(RESOURCES ${RESOURCES} tests/resources/resources.qrc)

file(GLOB TEST_CASES
        tests/components/jobs/*.cpp tests/components/jobs/*.h
        tests/components/parse/*.cpp tests/components/parse/*.h
        tests/components/project/*.cpp tests/components/project/*.h
        tests/components/repo/*.cpp tests/components/repo/*.h
        tests/components/settings/*.cpp tests/components/settings/*.h)

add_executable(${name_test} tests/Main.cpp ${COMPONENTS} ${WIDGETS} ${RESOURCES} ${TEST_CASES} ${VIEWS})
target_include_directories(${name_test} PRIVATE
        tests/components/jobs
        tests/components/parse
        tests/components/project
        tests/components/repo
        tests/components/settings
)

add_dependencies(${name_test} ${DEPS})

target_link_libraries(${name_test} PRIVATE Qt5::Test ${LIBS})

add_test(NAME ${name_test} COMMAND ${name_test})
