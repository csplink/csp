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
# 2023-04-17     xqyjlj       initial version
#

cmake_minimum_required(VERSION 3.5)

project(csp VERSION 0.0.0.1 LANGUAGES CXX)

set(CMAKE_AUTOUIC ON) # Qt about
set(CMAKE_AUTOMOC ON) # Qt Meta-Object Compiler
set(CMAKE_AUTORCC ON) # Qt resource system

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "GNU")
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -Wpedantic")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror -Wpedantic")
elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "MSVC")

endif ()

add_definitions(-DQT_NO_FOREACH)

find_package(QT NAMES Qt5 REQUIRED COMPONENTS Widgets OpenGL Test)
find_package(Qt5 REQUIRED COMPONENTS Widgets OpenGL Test)

find_package(QT NAMES Qt5 REQUIRED COMPONENTS LinguistTools)
find_package(Qt5 REQUIRED COMPONENTS LinguistTools)

include(cmake/git.cmake)

if (${CMAKE_BUILD_TYPE} MATCHES "Debug")
else ()
    string(TIMESTAMP BUILD_TIMESTAMP "%Y-%m-%d %H:%M:%S")
    get_git_tag(GIT_TAG)
    get_git_tag_long(GIT_TAG_LONG)
    get_git_branch(GIT_BRANCH)
    get_git_commit(GIT_COMMIT)
    get_git_commit_long(GIT_COMMIT_LONG)
    get_git_commit_date(GIT_COMMIT_DATE)
endif ()

enable_testing()

add_subdirectory(apps)
add_subdirectory(common)
add_subdirectory(components)
add_subdirectory(resources)
add_subdirectory(thirdparty)
add_subdirectory(tools)
