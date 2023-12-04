/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project_table.h
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
 *  2023-05-27     xqyjlj       initial version
 */

#ifndef COMMON_PROJECT_CSP_PROJECT_TABLE_H
#define COMMON_PROJECT_CSP_PROJECT_TABLE_H

#include "qtjson.h"
#include "qtyaml.h"

class project_table
{
  public:
    typedef QMap<QString, QString> pin_function_property_t;
    typedef QMap<QString, pin_function_property_t> pin_function_properties_t;

    typedef struct pin_config_struct
    {
        QString function;                            // pin selected function
        QString comment;                             // pin comment
        bool locked;                                 // pin locked
        pin_function_properties_t function_property; // pin function properties
    } pin_config_t;

    typedef struct core_struct
    {
        QString name;       // name
        QString hal;        // hal
        QString hal_name;   // hal.name
        QString package;    // package
        QString company;    // company
        QString type;       // type
        QString toolchains; // toolchains
    } core_t;

    typedef struct project_struct
    {
        QMap<QString, pin_config_t> pin_configs; // pin configs
        core_t core;                             // core configs
    } project_t;

  public:
    /**
     * @brief load project from json file
     * @param path: project file path
     * @return project
     */
    static project_t load_project(const QString &path);

    /**
     * @brief save project to json file
     * @param p: project
     * @param path: project file path
     */
    static void save_project(const project_t &p, const QString &path);

    /**
     * @brief dump project to json string
     * @param p: project
     * @return yaml string
     */
    static QString dump_project(const project_t &p);

  private:
    explicit project_table();
    ~project_table();
};

namespace YAML
{
template <> struct convert<project_table::project_t>
{
    static Node encode(const project_table::project_t &rhs)
    {
        Node node;
        node.force_insert("core", rhs.core);
        node.force_insert("pin_configs", rhs.pin_configs);
        return node;
    }

    static bool decode(const Node &node, project_table::project_t &rhs)
    {
        if (!node.IsMap() || node.size() < 1)
            return false;

        rhs.core = node["core"].as<project_table::core_t>();
        if (node["pin_configs"].IsDefined())
            rhs.pin_configs = node["pin_configs"].as<QMap<QString, project_table::pin_config_t>>();
        return true;
    }
};

template <> struct convert<project_table::pin_config_t>
{
    static Node encode(const project_table::pin_config_t &rhs)
    {
        Node node;
        node.force_insert("function", rhs.function);
        node.force_insert("comment", rhs.comment);
        node.force_insert("locked", rhs.locked);
        node.force_insert("function_property", rhs.function_property);
        return node;
    }

    static bool decode(const Node &node, project_table::pin_config_t &rhs)
    {
        if (!node.IsMap() || node.size() < 3)
            return false;

        rhs.function = node["function"].as<QString>();
        rhs.comment = node["comment"].as<QString>();
        rhs.locked = node["locked"].as<bool>();
        if (node["function_property"].IsDefined())
            rhs.function_property = node["function_property"].as<project_table::pin_function_properties_t>();
        return true;
    }
};

template <> struct convert<project_table::core_t>
{
    static Node encode(const project_table::core_t &rhs)
    {
        Node node;
        node.force_insert("name", rhs.name);
        node.force_insert("hal", rhs.hal);
        node.force_insert("hal_name", rhs.hal_name);
        node.force_insert("package", rhs.package);
        node.force_insert("company", rhs.company);
        node.force_insert("type", rhs.type);
        node.force_insert("toolchains", rhs.toolchains);
        return node;
    }

    static bool decode(const Node &node, project_table::core_t &rhs)
    {
        if (!node.IsMap() || node.size() < 7)
            return false;

        rhs.name = node["name"].as<QString>();
        rhs.hal = node["hal"].as<QString>();
        rhs.hal_name = node["hal_name"].as<QString>();
        rhs.package = node["package"].as<QString>();
        rhs.company = node["company"].as<QString>();
        rhs.type = node["type"].as<QString>();
        rhs.toolchains = node["toolchains"].as<QString>();
        return true;
    }
};
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(project_table::pin_config_struct, function, comment, locked, function_property)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(project_table::core_struct, name, hal, hal_name, package, company, type, toolchains)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(project_table::project_struct, core)
} // namespace nlohmann

#include <QDebug>

inline QDebug operator<<(QDebug debug, const project_table::project_t &rhs)
{
    const nlohmann::json j = rhs;
    debug << QString::fromStdString(j.dump(2));
    return debug;
}

inline QDebug operator<<(QDebug debug, const project_table::pin_config_t &rhs)
{
    const nlohmann::json j = rhs;
    debug << QString::fromStdString(j.dump(2));
    return debug;
}

inline QDebug operator<<(QDebug debug, const project_table::core_t &rhs)
{
    const nlohmann::json j = rhs;
    debug << QString::fromStdString(j.dump(2));
    return debug;
}

#endif // COMMON_PROJECT_CSP_PROJECT_TABLE_H
