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
#include <QProcess>

#include "os.h"
#include "path.h"
#include "project.h"

#include "config.h"
#include "xmake.h"

void project::init()
{
    if (_instance == nullptr)
    {
        _instance = new project();
    }
}

void project::deinit()
{
    delete _instance;
    _instance = nullptr;
}

project *project::get_instance()
{
    return _instance;
}

QString project::get_core(const core_attribute_type type) const
{
    QString value;

    switch (type)
    {
    case CORE_ATTRIBUTE_TYPE_HAL:
        value = _project.core.hal;
        break;
    case CORE_ATTRIBUTE_TYPE_TARGET:
        value = _project.core.target;
        break;
    case CORE_ATTRIBUTE_TYPE_PACKAGE:
        value = _project.core.package;
        break;
    case CORE_ATTRIBUTE_TYPE_COMPANY:
        value = _project.core.company;
        break;
    case CORE_ATTRIBUTE_TYPE_TYPE:
        value = _project.core.type;
        break;
    }

    return value;
}

void project::set_core(const core_attribute_type type, const QString &value)
{
    Q_ASSERT(!value.isEmpty());

    switch (type)
    {
    case CORE_ATTRIBUTE_TYPE_HAL:
        _project.core.hal = value;
        break;
    case CORE_ATTRIBUTE_TYPE_TARGET:
        _project.core.target = value;
        break;
    case CORE_ATTRIBUTE_TYPE_PACKAGE:
        _project.core.package = value;
        break;
    case CORE_ATTRIBUTE_TYPE_COMPANY:
        _project.core.company = value;
        break;
    case CORE_ATTRIBUTE_TYPE_TYPE:
        _project.core.type = value;
        break;
    }

    load_db();
}

QString project::get_path() const
{
    return _path;
}

void project::set_path(const QString &path)
{
    Q_ASSERT(!path.isEmpty());

    _path = path::absolute(path);
}

QString project::get_name() const
{
    return _project.name;
}

void project::set_name(const QString &name)
{
    Q_ASSERT(!name.isEmpty());

    _project.name = name;
}

void project::load_ips(const QString &hal, const QString &name)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());

    if (_ips.isEmpty())
    {
        ip_table::load_ips(&_ips, hal, name);
    }
}

void project::load_db()
{
    if (!_project.core.hal.isEmpty())
    {
        load_maps(_project.core.hal);
    }

    if (!_project.core.target.isEmpty() && !_project.core.hal.isEmpty())
    {
        load_ips(_project.core.hal, _project.core.target);
    }

    if (!_project.core.company.isEmpty() && !_project.core.hal.isEmpty())
    {
        load_chip_summary(_project.core.company, _project.core.target);
    }
}

ip_table::ips_t &project::get_ips()
{
    return _ips;
}

void project::load_maps(const QString &hal)
{
    Q_ASSERT(!hal.isEmpty());

    if (_maps.isEmpty())
    {
        map_table::load_maps(&_maps, hal);
    }
}

map_table::maps_t &project::get_maps()
{
    return _maps;
}

void project::load_chip_summary(const QString &company, const QString &name)
{
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    if (_chip_summary.name.isEmpty())
    {
        chip_summary_table::load_chip_summary(&_chip_summary, company, name);
    }
}

chip_summary_table::chip_summary_t &project::get_chip_summary()
{
    return _chip_summary;
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

void project::set_pin_locked(const QString &key, const bool locked)
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

void project::set_pin_config_fp(const QString &key, const QString &module, const QString &property,
                                const QString &value)
{
    Q_ASSERT(!key.isEmpty());
    Q_ASSERT(!module.isEmpty());
    Q_ASSERT(!property.isEmpty());
    Q_ASSERT(!value.isEmpty());

    emit signals_pin_function_property_changed(module, property, key,
                                               _project.pin_configs[key].function_property[module][property], value);
    _project.pin_configs[key].function_property[module][property] = value;
}

void project::clear_pin_config_fp(const QString &key, const QString &module, const QString &property)
{
    Q_ASSERT(!key.isEmpty());
    Q_ASSERT(!module.isEmpty());
    Q_ASSERT(!property.isEmpty());

    if (_project.pin_configs[key].function_property.contains(module))
    {
        if (_project.pin_configs[key].function_property[module].contains(property))
        {
            emit signals_pin_function_property_changed(
                module, property, key, _project.pin_configs[key].function_property[module][property], "");
            _project.pin_configs[key].function_property[module].remove(property);
        }
    }
}

void project::clear_pin_config_fp_module(const QString &key, const QString &module)
{
    Q_ASSERT(!key.isEmpty());
    Q_ASSERT(!module.isEmpty());

    if (_project.pin_configs[key].function_property.contains(module))
    {
        emit signals_pin_function_property_changed(module, "", key, "", "");
        _project.pin_configs[key].function_property.remove(module);
    }
}

project_table::pin_function_properties_t &project::get_pin_config_fps(const QString &key)
{
    Q_ASSERT(!key.isEmpty());

    return _project.pin_configs[key].function_property;
}

QString &project::get_pin_config_fp(const QString &key, const QString &module, const QString &property)
{
    Q_ASSERT(!key.isEmpty());
    Q_ASSERT(!module.isEmpty());
    Q_ASSERT(!property.isEmpty());

    return _project.pin_configs[key].function_property[module][property];
}

/***********************************************/

void project::load_project(const QString &path)
{
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    project_table::load_project(&_project, path);
    set_path(path);

    load_db();
}

void project::save_project(const QString &path)
{
    project_table::save_project(_project, path);
}

void project::save_project()
{
    Q_ASSERT(!_path.isEmpty());

    const auto p = path::directory(_path);
    if (!os::exists(p))
    {
        os::mkdir(p);
    }
    else
    {
        if (!os::isdir(p)) // check if it not is a directory
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

void project::clear_project()
{
    _project.pin_configs.clear();
    emit signals_project_clear();
}

void project::generate_code() const
{
    xmake *xmake_instance = xmake::get_instance();
    xmake_instance->csp_coder_log(_path, path::directory(_path), config::repositories_dir());
}

void project::build(const QString &mode) const
{
    xmake *xmake_instance = xmake::get_instance();
    xmake_instance->build_log(path::directory(_path), mode);
}
