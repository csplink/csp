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
# @file        git.cmake
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2023-06-24     xqyjlj       initial version
#

# get git tag
macro(get_git_tag _tag)
    find_package(Git QUIET)
    if (GIT_FOUND)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} describe --tags
                OUTPUT_VARIABLE ${_tag}
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    else ()
        set(${_tag} "unknown")
    endif ()

    if (${_tag} STREQUAL "")
        set(${_tag} "nil")
    endif ()
endmacro()

# get git tag long
macro(get_git_tag_long _tag)
    find_package(Git QUIET)
    if (GIT_FOUND)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} describe --tags --long
                OUTPUT_VARIABLE ${_tag}
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    else ()
        set(${_tag} "unknown")
    endif ()

    if (${_tag} STREQUAL "")
        set(${_tag} "nil")
    endif ()
endmacro()

# get git branch
macro(get_git_branch _branch)
    find_package(Git QUIET)
    if (GIT_FOUND)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} rev-parse --abbrev-ref HEAD
                OUTPUT_VARIABLE ${_branch}
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    else ()
        set(${_branch} "unknown")
    endif ()

    if (${_branch} STREQUAL "")
        set(${_branch} "nil")
    endif ()
endmacro()

# get git commit
macro(get_git_commit _commit)
    find_package(Git QUIET)
    if (GIT_FOUND)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} rev-parse --short HEAD
                OUTPUT_VARIABLE ${_commit}
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    else ()
        set(${_commit} "unknown")
    endif ()

    if (${_commit} STREQUAL "")
        set(${_commit} "nil")
    endif ()
endmacro()

# get git commit long
macro(get_git_commit_long _commit)
    find_package(Git QUIET)
    if (GIT_FOUND)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} rev-parse HEAD
                OUTPUT_VARIABLE ${_commit}
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    else ()
        set(${_commit} "unknown")
    endif ()

    if (${_commit} STREQUAL "")
        set(${_commit} "nil")
    endif ()
endmacro()

# get git hash
macro(get_git_commit_date _date)
    find_package(Git QUIET)
    if (GIT_FOUND)
        execute_process(
                COMMAND ${GIT_EXECUTABLE} log -1 --date=format:%Y%m%d%H%M%S --format=%ad
                OUTPUT_VARIABLE ${_date}
                OUTPUT_STRIP_TRAILING_WHITESPACE
                ERROR_QUIET
                WORKING_DIRECTORY
                ${CMAKE_CURRENT_SOURCE_DIR}
        )
    else ()
        set(${_date} "unknown")
    endif ()

    if (${_date} STREQUAL "")
        set(${_date} "nil")
    endif ()
endmacro()
