/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        MapTable.h
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

#ifndef CSP_REPO_MAP_TABLE_H
#define CSP_REPO_MAP_TABLE_H

#include <QMap>

class MapTable final
{
  public:
    typedef struct
    {
        QMap<QString, QString> comment;
    } ValueType;

    typedef struct group_struct
    {
        QMap<QString, QString> comment;
        QMap<QString, ValueType> values;
    } GroupType;

    typedef struct property_struct
    {
        QMap<QString, QString> display_name;
        QMap<QString, QString> description;
        QString category;
        bool readonly;
    } PropertyType;

    typedef struct
    {
        QMap<QString, GroupType> groups;
        QMap<QString, PropertyType> properties;
        QMap<QString, QString> total;
        QMap<QString, QString> reverse_total;
    } MapType;

    typedef QMap<QString, MapType> MapsType;

    static void loadMap(MapType *map, const QString &path);
    static void loadMap(MapType *map, const QString &hal, const QString &mapName);
    static void loadMaps(MapsType *maps, const QString &hal);

  private:
    explicit MapTable();
    ~MapTable();
};

#endif /** CSP_REPO_MAP_TABLE_H */
