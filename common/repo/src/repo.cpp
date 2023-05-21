/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        repo.cpp
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

#include "repo.h"
#include "config.h"

repo *repo::_instance = new repo();

repo::repo()
{
    _repository = repository_table::get_repository(config::repodir() + "/db/repository.yml");
}

repo::~repo() = default;

repo *repo::get_instance()
{
    return _instance;
}

const repository_table::repository_t *repo::get_repository() const
{
    return &_repository;
}
