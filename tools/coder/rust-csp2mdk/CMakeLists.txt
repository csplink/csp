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
# 2024-01-29     xqyjlj       initial version
#
set(project_name csp2mdk)
set(name custom_tools_coder_csp2mdk)

include(../../../cmake/check_rust_change.cmake)

file(GLOB_RECURSE SOURCES
        src/*.rs
        template/*
        Cargo.lock
        Cargo.toml
)

if (WIN32)
    set(CSP2MDK_EXE "csp2mdk.exe")
else ()
    set(CSP2MDK_EXE "csp2mdk")
endif ()

set(source_file ${CMAKE_CURRENT_BINARY_DIR}/${CSP2MDK_EXE})
set(target_file ${CSP_EXE_DIR}/xmake/tools/scripts/tasks/csp-project/mdk/${CSP2MDK_EXE})

check_rust_change(
        SOURCE_FILES ${SOURCES}
        TARGET_FILE ${source_file}
        IS_CHANGED is_project_changed
)

if (${is_project_changed})
    if (${CMAKE_BUILD_TYPE} MATCHES "Debug")
        set(build_type "dev")
    else ()
        set(build_type "release")
    endif ()

    corrosion_import_crate(
            MANIFEST_PATH "${CMAKE_CURRENT_SOURCE_DIR}/Cargo.toml"
            LOCKED
            PROFILE ${build_type}
    )
else ()
    message(STATUS "because target \"${name}\" has not been modified, we do not compile it")
endif ()

add_custom_command(OUTPUT ${target_file}
        POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${source_file} ${target_file}
        DEPENDS ${source_file}
)

add_custom_target(${name}
        DEPENDS ${target_file}
)

if (${is_project_changed})
    add_dependencies(${name}
            _cargo-build_${project_name}
    )
endif ()