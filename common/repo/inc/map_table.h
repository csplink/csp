/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        map_table.h
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

#ifndef CSP_MAP_TABLE_H
#define CSP_MAP_TABLE_H

#include <QMap>

class map_table final
{
  public:
    typedef struct value_struct
    {
        QMap<QString, QString> comment;
    } value_t;

    typedef struct group_struct
    {
        QMap<QString, QString> comment;
        QMap<QString, value_t> values;
    } group_t;

    typedef struct property_struct
    {
        QMap<QString, QString> display_name;
        QMap<QString, QString> description;
        QString category;
        bool readonly;
    } property_t;

    typedef struct
    {
        QMap<QString, group_t> groups;
        QMap<QString, property_t> properties;
        QMap<QString, QString> total;
        QMap<QString, QString> reverse_total;
    } map_t;

    typedef QMap<QString, map_t> maps_t;

  public:
    static map_t load_map(const QString &path);
    static map_t load_map(const QString &hal, const QString &map);
    static maps_t load_maps(const QString &hal);

  private:
    explicit map_table();
    ~map_table();
};

#endif // CSP_MAP_TABLE_H
