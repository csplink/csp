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
# @file        check_rust_change.cmake
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-02-06     xqyjlj       initial version
#

include(CMakeParseArguments)

# detect rust change
function(check_rust_change)
    CMAKE_PARSE_ARGUMENTS(
            CHECK "" "TARGET_FILE;IS_CHANGED"
            "SOURCE_FILES"
            ${ARGN}
    )
    if (EXISTS ${CHECK_TARGET_FILE})
        file(TIMESTAMP ${CHECK_TARGET_FILE} current_now_timestamp)
        file(TIMESTAMP ${CHECK_TARGET_FILE} current_now_timestamp_old)
        foreach (file IN LISTS CHECK_SOURCE_FILES)
            file(TIMESTAMP ${file} file_timestamp)
            string(COMPARE GREATER ${file_timestamp} ${current_now_timestamp} is_update)
            if (${is_update})
                set(current_now_timestamp ${file_timestamp})
            endif ()
        endforeach ()
        string(COMPARE GREATER ${current_now_timestamp} ${current_now_timestamp_old} is_update)
        set(${CHECK_IS_CHANGED} ${is_update} PARENT_SCOPE)
    else ()
        set(${CHECK_IS_CHANGED} ON PARENT_SCOPE)
    endif ()
endfunction()
