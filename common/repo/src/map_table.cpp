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
#include <QFileInfo>

#include "Config.h"
#include "map_table.h"
#include "os.h"
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

        auto group_i = map->groups.constBegin();
        while (group_i != map->groups.constEnd())
        {
            auto values = group_i.value().values;
            auto values_i = values.constBegin();
            while (values_i != values.constEnd())
            {
                const QString &name = values_i.key();
                const value_t &value = values_i.value();
                map->total.insert(name, value.comment[Config::language()]);
                map->reverse_total.insert(value.comment[Config::language()], name);
                ++values_i;
            }
            ++group_i;
        }
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

    const QString path = QString("%1/db/hal/%2/map/%3.yml").arg(Config::repodir(), hal.toLower(), map_name.toLower());
    return load_map(map, path);
}

void map_table::load_maps(maps_t *maps, const QString &hal)
{
    Q_ASSERT(maps != nullptr);
    Q_ASSERT(!hal.isEmpty());

    const QString p = QString("%1/db/hal/%2/map").arg(Config::repodir(), hal.toLower());
    for (const QString &file : os::files(p, QString("*.yml")))
    {
        map_t map;
        load_map(&map, file);
        const QFileInfo info(file);
        auto basename = info.baseName().toLower();
        maps->insert(basename, map);
    }

    const QStringList list = { "gpio" };
    for (const QString &file : list)
    {
        map_t map;
        load_map(&map, QString(":/lib/repo/db/map/%1.yml").arg(file));
        const QFileInfo info(file);
        const QString basename = info.baseName().toLower();
        if (maps->contains(basename))
        {
            map_t &ref_map = (*maps)[basename];
            auto group_i = map.groups.constBegin();
            while (group_i != map.groups.constEnd())
            {
                ref_map.groups.insert(group_i.key(), group_i.value());
                ++group_i;
            }
            auto properties_i = map.properties.constBegin();
            while (properties_i != map.properties.constEnd())
            {
                ref_map.properties.insert(properties_i.key(), properties_i.value());
                ++properties_i;
            }
            auto total_i = map.total.constBegin();
            while (total_i != map.total.constEnd())
            {
                ref_map.total.insert(total_i.key(), total_i.value());
                ++total_i;
            }
            auto reverse_total_i = map.reverse_total.constBegin();
            while (reverse_total_i != map.reverse_total.constEnd())
            {
                ref_map.reverse_total.insert(reverse_total_i.key(), reverse_total_i.value());
                ++reverse_total_i;
            }
        }
        else
        {
            maps->insert(basename, map);
        }
    }
}
