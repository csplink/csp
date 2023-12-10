/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        map_table.cpp
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
 *  2023-06-17     xqyjlj       initial version
 */
#include <QDebug>
#include <QFile>

#include "config.h"
#include "map_table.h"
#include "os.h"
#include "path.h"
#include "qtjson.h"
#include "qtyaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE(map_table::value_t, comment)
YAML_DEFINE_TYPE_NON_INTRUSIVE(map_table::group_t, comment, values)
YAML_DEFINE_TYPE_NON_INTRUSIVE(map_table::property_t, display_name, description, category, readonly)
YAML_DEFINE_TYPE_NON_INTRUSIVE(map_table::map_t, groups, properties)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(map_table::value_t, comment)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(map_table::group_t, comment, values)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(map_table::property_t, display_name, description, category, readonly)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(map_table::map_t, groups, properties, total, reverse_total)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(map_table::value_t)
QT_DEBUG_ADD_TYPE(map_table::group_t)
QT_DEBUG_ADD_TYPE(map_table::property_t)
QT_DEBUG_ADD_TYPE(map_table::map_t)

map_table::map_table() = default;

map_table::~map_table() = default;

void map_table::load_map(map_t *map, const QString &path)
{
    Q_ASSERT(map != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const YAML::Node yaml_data = YAML::Load(buffer);
        YAML::convert<map_t>::decode(yaml_data, *map);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

void map_table::load_map(map_t *map, const QString &hal, const QString &map_name)
{
    Q_ASSERT(map != nullptr);
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!map_name.isEmpty());

    const QString path = QString("%1/db/hal/%2/map/%3.yml").arg(config::repodir(), hal.toLower(), map_name.toLower());
    return load_map(map, path);
}

void map_table::load_maps(maps_t *maps, const QString &hal)
{
    Q_ASSERT(maps != nullptr);
    Q_ASSERT(!hal.isEmpty());

    const QString p = QString("%1/db/hal/%2/map").arg(config::repodir(), hal.toLower());
    for (const QString &file : os::files(p, QString("*.yml")))
    {
        map_t map;
        load_map(&map, file);
        auto basename = path::basename(file).toLower();
        maps->insert(basename, map);
    }
}
