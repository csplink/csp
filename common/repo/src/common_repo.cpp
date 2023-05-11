/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        common_repo.cpp
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the GNU General Public License v. 3 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.gnu.org/licenses/gpl-3.0.html
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-05-11     xqyjlj       initial version
 */

#include "common_repo.h"

common_repo *common_repo::_common_repo =new (std::nothrow) common_repo(); // NOLINT(cppcoreguidelines-interfaces-global-init)

common_repo::common_repo() = default;

common_repo::~common_repo() = default;

common_repo *common_repo::get_instance()
{
    return _common_repo;
}
