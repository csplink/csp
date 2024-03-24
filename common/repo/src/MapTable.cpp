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
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::ValueType, Comment)
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::GroupType, Comment, Values)
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::PropertyType, DisplayName, Description, Category, Readonly)
YAML_DEFINE_TYPE_NON_INTRUSIVE(MapTable::MapType, Groups, Properties)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::ValueType, Comment)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::GroupType, Comment, Values)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::PropertyType, DisplayName, Description, Category, Readonly)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(MapTable::MapType, Groups, Properties, Total, ReverseTotal)
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

            auto group_i = map->Groups.constBegin();
            while (group_i != map->Groups.constEnd())
            {
                auto values = group_i.value().Values;
                auto values_i = values.constBegin();
                while (values_i != values.constEnd())
                {
                    const QString &name = values_i.key();
                    const ValueType &value = values_i.value();
                    map->Total.insert(name, value.Comment[Config::language()]);
                    map->ReverseTotal.insert(value.Comment[Config::language()], name);
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
                    auto group_i = map.Groups.constBegin();
                    while (group_i != map.Groups.constEnd())
                    {
                        ref_map.Groups.insert(group_i.key(), group_i.value());
                        ++group_i;
                    }
                    auto properties_i = map.Properties.constBegin();
                    while (properties_i != map.Properties.constEnd())
                    {
                        ref_map.Properties.insert(properties_i.key(), properties_i.value());
                        ++properties_i;
                    }
                    auto total_i = map.Total.constBegin();
                    while (total_i != map.Total.constEnd())
                    {
                        ref_map.Total.insert(total_i.key(), total_i.value());
                        ++total_i;
                    }
                    auto reverse_total_i = map.ReverseTotal.constBegin();
                    while (reverse_total_i != map.ReverseTotal.constEnd())
                    {
                        ref_map.ReverseTotal.insert(reverse_total_i.key(), reverse_total_i.value());
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
