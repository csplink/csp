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
# 2023-04-21     xqyjlj       initial version
#

file(GLOB_RECURSE SOURCES
        *.cpp)

add_library(common_utils STATIC ${SOURCES})
target_link_libraries(common_utils PUBLIC Qt5::Widgets)
target_include_directories(common_utils PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)
