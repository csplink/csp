/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        MapTable.cpp
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
#include <QDir>
#include <QFile>
#include <QFileInfo>

#include "Config.h"
#include "MapTable.h"
#include "QtJson.h"
#include "QtYaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::ValueType, comment)
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::GroupType, comment, values)
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::PropertyType, display_name, description, category, readonly)
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::MapType, groups, properties)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::ValueType, comment)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::GroupType, comment, values)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::PropertyType, display_name, description, category, readonly)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::MapType, groups, properties, total, reverse_total)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(MapTable::ValueType)
QT_DEBUG_ADD_TYPE(MapTable::GroupType)
QT_DEBUG_ADD_TYPE(MapTable::PropertyType)
QT_DEBUG_ADD_TYPE(MapTable::MapType)

MapTable::MapTable() = default;

MapTable::~MapTable() = default;

void MapTable::loadMap(MapType *map, const QString &path)
{
    if (map != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<MapType>::decode(yaml_data, *map);
            }
            catch (std::exception &e)
            {
                const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
                qCritical().noquote() << str;
                throw;
            }

            file.close();

            auto group_i = map->groups.constBegin();
            while (group_i != map->groups.constEnd())
            {
                auto values = group_i.value().values;
                auto values_i = values.constBegin();
                while (values_i != values.constEnd())
                {
                    const QString &name = values_i.key();
                    const ValueType &value = values_i.value();
                    map->total.insert(name, value.comment[Config::language()]);
                    map->reverse_total.insert(value.comment[Config::language()], name);
                    ++values_i;
                }
                ++group_i;
            }
        }
        else
        {
            /** TODO: failed */
        }
    }
    else
    {
        /** TODO: failed */
    }
}

void MapTable::loadMap(MapType *map, const QString &hal, const QString &mapName)
{
    if (map != nullptr)
    {
        if (!hal.isEmpty() && !mapName.isEmpty())
        {
            const QString path = QString("%1/db/hal/%2/map/%3.yml").arg(Config::repoDir(), hal.toLower(), mapName.toLower());
            loadMap(map, path);
        }
        else
        {
            /** TODO: failed */
        }
    }
    else
    {
        /** TODO: failed */
    }
}

void MapTable::loadMaps(MapsType *maps, const QString &hal)
{
    if (maps != nullptr)
    {
        if (!hal.isEmpty())
        {
            const QString path = QString("%1/db/hal/%2/map").arg(Config::repoDir(), hal.toLower());
            const QDir dir(path);
            QFileInfoList files = dir.entryInfoList({ "*.yml" }, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
            for (const QFileInfo &file : files)
            {
                MapType map;
                loadMap(&map, file.absoluteFilePath());
                const QFileInfo info(file);
                auto basename = info.baseName().toLower();
                maps->insert(basename, map);
            }

            const QStringList list = { "gpio" };
            for (const QString &file : list)
            {
                MapType map;
                loadMap(&map, QString(":/lib/repo/db/map/%1.yml").arg(file));
                const QFileInfo info(file);
                const QString basename = info.baseName().toLower();
                if (maps->contains(basename))
                {
                    MapType &ref_map = (*maps)[basename];
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
        else
        {
            /** TODO: failed */
        }
    }
    else
    {
        /** TODO: failed */
    }
}
