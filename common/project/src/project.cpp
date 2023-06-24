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

#include <QDebug>

#include "os.h"
#include "path.h"
#include "project.h"

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

    _project.core[key] = value;
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

ip_table::ips_t &project::load_ips(const QString &hal, const QString &name)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());

    _ips = ip_table::load_ips(hal, name);
    return _ips;
}

ip_table::ips_t &project::get_ips()
{
    return _ips;
}

map_table::maps_t &project::load_maps(const QString &hal)
{
    Q_ASSERT(!hal.isEmpty());

    _maps = map_table::load_maps(hal);
    return _maps;
}

map_table::maps_t &project::get_maps()
{
    return _maps;
}

/******************* pin ************************/
project_table::pin_config_t &project::get_pin_config(const QString &key)
{
    Q_ASSERT(!key.isEmpty());
    return _project.pin_configs[key];
}

void project::set_pin_comment(const QString &key, const QString &comment)
{
    Q_ASSERT(!key.isEmpty());
    emit signals_pin_property_changed("comment", key, _project.pin_configs[key].comment, comment);
    _project.pin_configs[key].comment = comment;
}

QString &project::get_pin_comment(const QString &key)
{
    Q_ASSERT(!key.isEmpty());
    return _project.pin_configs[key].comment;
}

void project::set_pin_function(const QString &key, const QString &function)
{
    Q_ASSERT(!key.isEmpty());
    emit signals_pin_property_changed("function", key, _project.pin_configs[key].function, function);
    _project.pin_configs[key].function = function;
}

QString &project::get_pin_function(const QString &key)
{
    Q_ASSERT(!key.isEmpty());
    return _project.pin_configs[key].function;
}

void project::set_pin_locked(const QString &key, bool locked)
{
    Q_ASSERT(!key.isEmpty());
    emit signals_pin_property_changed("locked", key, _project.pin_configs[key].locked, locked);
    _project.pin_configs[key].locked = locked;
}

bool project::get_pin_locked(const QString &key)
{
    Q_ASSERT(!key.isEmpty());
    return _project.pin_configs[key].locked;
}

/***********************************************/

void project::load_project(const QString &path)
{
    _project = project_table::load_project(path);
    _path    = path;

    load_maps(_project.core[CSP_PROJECT_CORE_HAL]);
    load_ips(_project.core[CSP_PROJECT_CORE_HAL], _project.core[CSP_PROJECT_CORE_HAL_NAME]);
}

void project::save_project(const QString &path)
{
    project_table::save_project(_project, path);
}

void project::save_project()
{
    Q_ASSERT(!_path.isEmpty());

    auto p = path::directory(_path);
    if (!os::exists(p))
    {
        os::mkdir(p);
    }
    else
    {
        if (!os::isdir(p))  // check if it not is a directory
        {
            os::show_error_and_exit(tr("The project <%1> path is not a directory!").arg(p));
        }
    }
    project_table::save_project(_project, _path);
}

QString project::dump_project()
{
    return project_table::dump_project(_project);
}
