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
# 2023-12-17     xqyjlj       initial version
#
set(name custom_res_repo)
set(depends_list)

file(GLOB_RECURSE DB_SOURCES
        db/*.yml
)

foreach (source_file ${DB_SOURCES})
    file(RELATIVE_PATH relative_path ${CMAKE_CURRENT_SOURCE_DIR} ${source_file})
    set(target_file ${CSP_EXE_DIR}/repo/${relative_path})
    add_custom_command(OUTPUT ${target_file}
            POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy_if_different ${source_file} ${target_file}
            DEPENDS ${source_file}
    )
    list(APPEND depends_list ${target_file})
endforeach ()

add_custom_target(${name}
        DEPENDS ${depends_list}
)