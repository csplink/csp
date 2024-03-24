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
        QMap<QString, QString> Comment;
    } ValueType;

    typedef struct
    {
        QMap<QString, QString> Comment;
        QMap<QString, ValueType> Values;
    } GroupType;

    typedef struct
    {
        QMap<QString, QString> DisplayName;
        QMap<QString, QString> Description;
        QString Category;
        bool Readonly;
    } PropertyType;

    typedef struct
    {
        QMap<QString, GroupType> Groups;
        QMap<QString, PropertyType> Properties;
        QMap<QString, QString> Total;
        QMap<QString, QString> ReverseTotal;
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
