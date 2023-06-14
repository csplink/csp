/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project.cpp
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
 *  2023-05-26     xqyjlj       initial version
 */

#include "project.h"

using namespace csp;

project *project::_instance = new project();

project::project() = default;

project::~project() = default;

project *project::get_instance()
{
    return _instance;
}

QString project::get_core(const QString &key) const
{
    Q_ASSERT(!key.isEmpty());

    if (_project.core.contains(key))
        return _project.core[key];
    else
        return "";
}

void project::set_core(const QString &key, const QString &value)
{
    Q_ASSERT(!key.isEmpty());
    Q_ASSERT(!value.isEmpty());

    if (_project.core.contains(key))
        _project.core[key] = value;
    else
        _project.core.insert(key, value);
}

QString project::get_path() const
{
    return _path;
}

void project::set_path(const QString &path)
{
    Q_ASSERT(!path.isEmpty());

    _path = path;
}

project_table::pin_config_t &project::get_pin_config(const QString &key)
{
    return _project.pin_configs[key];
}
