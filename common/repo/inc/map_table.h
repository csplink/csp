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

#include "config.h"
#include "qtyaml.h"

namespace csp {

class map_table {
public:
    typedef struct
    {
        QMap<QString, QString> comment;
    } value_t;

    typedef struct
    {
        QMap<QString, QString> comment;
        QMap<QString, value_t> values;
    } group_t;

    typedef struct
    {
        QMap<QString, QString> display_name;
        QMap<QString, QString> description;
        QString                category;
        bool                   readonly;
    } property_t;

    typedef struct
    {
        QMap<QString, group_t>    groups;
        QMap<QString, property_t> properties;
        QMap<QString, QString>    total;
    } map_t;

    typedef QMap<QString, map_t> maps_t;

public:
    static map_t  load_map(const QString &path);
    static map_t  load_map(const QString &hal, const QString &map);
    static maps_t load_maps(const QString &hal);

private:
    explicit map_table();
    ~map_table();
};

}  // namespace csp

namespace YAML {

template <> struct convert<csp::map_table::value_t>
{
    static Node encode(const csp::map_table::value_t &rhs)
    {
        Node node;
        node.force_insert("Comment", rhs.comment);
        return node;
    }

    static bool decode(const Node &node, csp::map_table::value_t &rhs)
    {
        if (!node.IsMap() || node.size() != 1)
            return false;

        rhs.comment = node["Comment"].as<QMap<QString, QString>>();
        return true;
    }
};

template <> struct convert<csp::map_table::group_t>
{
    static Node encode(const csp::map_table::group_t &rhs)
    {
        Node node;
        node.force_insert("Comment", rhs.comment);
        node.force_insert("Values", rhs.values);
        return node;
    }

    static bool decode(const Node &node, csp::map_table::group_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.comment = node["Comment"].as<QMap<QString, QString>>();
        rhs.values  = node["Values"].as<QMap<QString, csp::map_table::value_t>>();
        return true;
    }
};

template <> struct convert<csp::map_table::property_t>
{
    static Node encode(const csp::map_table::property_t &rhs)
    {
        Node node;
        node.force_insert("DisplayName", rhs.display_name);
        node.force_insert("Description", rhs.description);
        node.force_insert("Category", rhs.category);
        node.force_insert("ReadOnly", rhs.readonly);
        return node;
    }

    static bool decode(const Node &node, csp::map_table::property_t &rhs)
    {
        if (!node.IsMap() || node.size() != 4)
            return false;

        rhs.display_name = node["DisplayName"].as<QMap<QString, QString>>();
        rhs.description  = node["Description"].as<QMap<QString, QString>>();
        rhs.category     = node["Category"].as<QString>();
        rhs.readonly     = node["ReadOnly"].as<bool>();
        return true;
    }
};

template <> struct convert<csp::map_table::map_t>
{
    static Node encode(const csp::map_table::map_t &rhs)
    {
        Node node;
        node.force_insert("Groups", rhs.groups);
        node.force_insert("Properties", rhs.properties);
        return node;
    }

    static bool decode(const Node &node, csp::map_table::map_t &rhs)
    {
        if (!node.IsMap() || node.size() != 2)
            return false;

        rhs.groups     = node["Groups"].as<QMap<QString, csp::map_table::group_t>>();
        rhs.properties = node["Properties"].as<QMap<QString, csp::map_table::property_t>>();

        auto group_i = rhs.groups.constBegin();
        while (group_i != rhs.groups.constEnd())
        {
            auto values   = group_i.value().values;
            auto values_i = values.constBegin();
            while (values_i != values.constEnd())
            {
                auto name  = values_i.key();
                auto value = values_i.value();
                rhs.total.insert(name, value.comment[csp::config::language()]);
                values_i++;
            }
            group_i++;
        }

        return true;
    }
};
}  // namespace YAML

#endif  // CSP_MAP_TABLE_H
