/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Repo.cpp
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

#include "Repo.h"
#include "Config.h"

repo::repo()
{
    RepositoryTable::loadRepository(&repository_, Config::repoDir() + "/db/repository.yml");
}

repo::~repo() = default;

void repo::init()
{
    if (instance_ == nullptr)
    {
        instance_ = new repo();
    }
}

void repo::deinit()
{
    delete instance_;
    instance_ = nullptr;
}

repo *repo::getInstance()
{
    return instance_;
}

const RepositoryTable::RepositoryType *repo::getRepository() const
{
    return &repository_;
}
