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
# 2023-05-26     xqyjlj       initial version
#
set(name CspProject)

file(GLOB_RECURSE SOURCES
        inc/*.h
        src/*.cpp
        resources/*.qrc)

set(TS_FILES
        ./resources/translations/${name}.zh_CN.ts
        ./resources/translations/${name}.zh_TW.ts)

if (DEFINED CSP_EXE_DIR)
    foreach (TS_FILE ${TS_FILES})
        set_source_files_properties(${TS_FILE} PROPERTIES OUTPUT_LOCATION ${CSP_EXE_DIR}/translations)
    endforeach ()
endif ()

qt5_create_translation(QM_FILES ${SOURCES}
        ${CMAKE_CURRENT_SOURCE_DIR}/inc
        ${TS_FILES})

add_library(${name} STATIC ${SOURCES} ${QM_FILES} ${TS_FILES})
target_link_libraries(${name} PUBLIC CspParse CspRepo CspTools CspXMake CspConfig Qt5::Concurrent Qt5::Widgets)
target_include_directories(${name} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)

##########################################################################

file(GLOB_RECURSE TEST_CASES
        test/*.cpp)

foreach (TEST_CASE ${TEST_CASES})
    get_filename_component(TARGET_NAME ${TEST_CASE} NAME_WE)
    add_executable(${TARGET_NAME} ${TEST_CASE} test/res/res.qrc)
    target_link_libraries(${TARGET_NAME} PRIVATE Qt5::Test ${name})
    add_test(NAME ${TARGET_NAME} COMMAND ${TARGET_NAME})
endforeach ()

