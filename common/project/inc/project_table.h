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

#include "qtyaml.h"

#define CSP_PROJECT_CORE_NAME "name"
#define CSP_PROJECT_CORE_HAL "hal"
#define CSP_PROJECT_CORE_HAL_NAME "hal.name"
#define CSP_PROJECT_CORE_PACKAGE "package"
#define CSP_PROJECT_CORE_COMPANY "company"
#define CSP_PROJECT_CORE_TYPE "type"

class project_table
{
  public:
    typedef QMap<QString, QString> pin_function_property_t;
    typedef QMap<QString, pin_function_property_t> pin_function_properties_t;

    typedef struct
    {
        QString function;             // pin selected function
        QString comment;              // pin comment
        bool locked;                  // pin locked
        pin_function_properties_t fp; // pin function properties
    } pin_config_t;

    typedef struct
    {
        QMap<QString, pin_config_t> pin_configs; // pin configs
        QMap<QString, QString> core;             // core configs
    } project_t;

  public:
    /**
     * @brief load project from yaml file
     * @param path: project file path
     * @return project
     */
    static project_t load_project(const QString &path);

    /**
     * @brief save project to yaml file
     * @param p: project
     * @param path: project file path
     */
    static void save_project(const project_t &p, const QString &path);

    /**
     * @brief dump project to yaml string
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
        node.force_insert("Core", rhs.core);
        node.force_insert("PinConfigs", rhs.pin_configs);
        return node;
    }

    static bool decode(const Node &node, project_table::project_t &rhs)
    {
        if (!node.IsMap() || node.size() < 1)
            return false;

        rhs.core = node["Core"].as<QMap<QString, QString>>();
        if (node["PinConfigs"].IsDefined())
            rhs.pin_configs = node["PinConfigs"].as<QMap<QString, project_table::pin_config_t>>();
        return true;
    }
};

template <> struct convert<project_table::pin_config_t>
{
    static Node encode(const project_table::pin_config_t &rhs)
    {
        Node node;
        node.force_insert("Function", rhs.function);
        node.force_insert("Comment", rhs.comment);
        node.force_insert("Locked", rhs.locked);
        node.force_insert("FunctionProperty", rhs.fp);
        return node;
    }

    static bool decode(const Node &node, project_table::pin_config_t &rhs)
    {
        if (!node.IsMap() || node.size() < 3)
            return false;

        rhs.function = node["Function"].as<QString>();
        rhs.comment = node["Comment"].as<QString>();
        rhs.locked = node["Locked"].as<bool>();
        if (node["FunctionProperty"].IsDefined())
            rhs.fp = node["FunctionProperty"].as<project_table::pin_function_properties_t>();
        return true;
    }
};
} // namespace YAML

#endif // COMMON_PROJECT_CSP_PROJECT_TABLE_H
