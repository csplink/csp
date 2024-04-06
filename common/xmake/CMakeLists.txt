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
# 2024-03-16     xqyjlj       initial version
#
set(name CspXMake)

file(GLOB_RECURSE SOURCES
        inc/*.h
        src/*.cpp
        resources/*.qrc)

add_library(${name} STATIC ${SOURCES})
target_link_libraries(${name} PUBLIC CspConfig)
target_include_directories(${name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)

##########################################################################

file(GLOB_RECURSE TEST_CASES
        test/*.cpp)

foreach (TEST_CASE ${TEST_CASES})
    get_filename_component(TARGET_NAME ${TEST_CASE} NAME_WE)
    add_executable(${TARGET_NAME} ${TEST_CASE})
    target_compile_definitions(${TARGET_NAME} PRIVATE -DCSP_EXE_DIR=\"${CSP_EXE_DIR}\")
    target_link_libraries(${TARGET_NAME} PRIVATE Qt5::Test ${name})
    add_test(NAME ${TARGET_NAME} COMMAND ${TARGET_NAME})
endforeach ()
