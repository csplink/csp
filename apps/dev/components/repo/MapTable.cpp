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
#include <QDir>
#include <QFile>
#include <QFileInfo>

#include "MapTable.h"
#include "QtJson.h"
#include "QtYaml.h"
#include "Settings.h"

namespace QT_YAML
{
QT_YAML_GEN_PARSE_CODE(MapTable::ValueType, Comment)
QT_YAML_GEN_PARSE_CODE(MapTable::GroupType, Comment, Values)
QT_YAML_GEN_PARSE_CODE(MapTable::PropertyType, DisplayName, Description, Category, Readonly)
QT_YAML_GEN_PARSE_CODE(MapTable::MapType, Groups, Properties)
} // namespace QT_YAML

namespace QT_JSON
{
QT_JSON_GEN_PARSE_CODE(MapTable::ValueType, Comment)
QT_JSON_GEN_PARSE_CODE(MapTable::GroupType, Comment, Values)
QT_JSON_GEN_PARSE_CODE(MapTable::PropertyType, DisplayName, Description, Category, Readonly)
QT_JSON_GEN_PARSE_CODE(MapTable::MapType, Groups, Properties, Total, ReverseTotal)
} // namespace QT_JSON

QT_DEBUG_ADD_TYPE(MapTable::ValueType)
QT_DEBUG_ADD_TYPE(MapTable::GroupType)
QT_DEBUG_ADD_TYPE(MapTable::PropertyType)
QT_DEBUG_ADD_TYPE(MapTable::MapType)

MapTable::MapTable() = default;

MapTable::~MapTable() = default;

bool MapTable::loadMap(MapType *map, const QString &path)
{
    bool rtn = false;
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
                rtn = true;
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
                    map->Total.insert(name, value.Comment[Settings.language()]);
                    map->ReverseTotal.insert(value.Comment[Settings.language()], name);
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
    return rtn;
}

bool MapTable::loadMap(MapType *map, const QString &hal, const QString &mapName)
{
    bool rtn = false;
    if (map != nullptr)
    {
        if (!hal.isEmpty() && !mapName.isEmpty())
        {
            const QString path =
                QString("%1/hal/%2/map/%3.yml").arg(Settings.database(), hal.toLower(), mapName.toLower());
            rtn = loadMap(map, path);
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
    return rtn;
}

bool MapTable::loadMaps(MapsType *maps, const QString &hal)
{
    bool rtn = false;
    if (maps != nullptr)
    {
        if (!hal.isEmpty())
        {
            const QString path = QString("%1/hal/%2/map").arg(Settings.database(), hal.toLower());
            const QDir dir(path);
            QFileInfoList files = dir.entryInfoList({"*.yml"}, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
            if (!files.isEmpty())
            {
                for (const QFileInfo &file : files)
                {
                    MapType map;
                    rtn = loadMap(&map, file.absoluteFilePath());
                    if (!rtn)
                    {
                        break;
                    }
                    const QFileInfo info(file);
                    auto basename = info.baseName().toLower();
                    maps->insert(basename, map);
                }
            }
            else
            {
                rtn = true;
            }

            static const QStringList list = {"GPIO"};
            if (rtn)
            {
                for (const QString &module : list)
                {
                    MapType map;
                    loadMap(&map, QString(":/database/map/%1.yml").arg(module.toLower()));
                    if (maps->contains(module))
                    {
                        MapType &ref_map = (*maps)[module];
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
                        maps->insert(module, map);
                    }
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
    return rtn;
}
