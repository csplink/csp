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
# 2023-04-19     xqyjlj       initial version
#
set(name compat_layer)

add_library(${name} INTERFACE)
target_link_libraries(${name} INTERFACE yaml-cpp Qt5::Core nlohmann-json)
target_include_directories(${name} INTERFACE
        ${CMAKE_CURRENT_SOURCE_DIR}/yaml-cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/nlohmann-json
)

##########################################################################

file(GLOB_RECURSE TESTCASES
        test/*.cpp)

foreach (TESTCASE ${TESTCASES})
    get_filename_component(TARGET_NAME ${TESTCASE} NAME_WE)
    add_executable(${TARGET_NAME} ${TESTCASE}
            test/testcase_qtjson.cpp)
    target_link_libraries(${TARGET_NAME} PRIVATE Qt5::Test ${name})
    add_test(NAME ${TARGET_NAME} COMMAND ${TARGET_NAME})
endforeach ()

