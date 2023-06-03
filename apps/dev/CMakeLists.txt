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

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")

set(CSP_EXE_DIR ${CMAKE_CURRENT_BINARY_DIR} CACHE INTERNAL "csp exe file dir")

file(GLOB_RECURSE DIALOGS
        dialogs/*.ui
        dialogs/*.h
        dialogs/*.cpp)

file(GLOB_RECURSE HEADERS
        inc/*.h)

file(GLOB_RECURSE SOURCES
        src/*.cpp)

file(GLOB_RECURSE RESOURCES
        resources/*.qrc
        resources/*.rc)

file(GLOB_RECURSE VIEWS
        views/*.ui
        views/*.h
        views/*.cpp)

set(TS_FILES
        ./resources/translations/${name}.zh_CN.ts
        ./resources/translations/${name}.zh_TW.ts)

set(PROJECT_SOURCES ${DIALOGS} ${HEADERS} ${SOURCES} ${RESOURCES} ${VIEWS} ${TS_FILES})

include_directories(
        dialogs
        inc
        views
${CMAKE_DIR})

foreach (TS_FILE ${TS_FILES})
    set_source_files_properties(${TS_FILE} PROPERTIES OUTPUT_LOCATION
            ${CMAKE_CURRENT_BINARY_DIR}/translations)
endforeach ()

qt5_create_translation(QM_FILES ${CMAKE_CURRENT_SOURCE_DIR} ${TS_FILES})

add_executable(${name} ${PROJECT_SOURCES} ${QM_FILES})
target_link_libraries(${name} PRIVATE Qt5::Widgets repo core project)
