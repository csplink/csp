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

#define CSP_PROJECT_CORE_NAME     "name"
#define CSP_PROJECT_CORE_HAL      "hal"
#define CSP_PROJECT_CORE_HAL_NAME "hal.name"
#define CSP_PROJECT_CORE_PACKAGE  "package"

namespace csp {
class project_table {
public:
    typedef struct
    {
        QMap<QString, QString> core;
    } project_t;

public:
    static project_t load_project(const QString &path);
    static void      save_project(const project_t &p, const QString &path);
    static QString   dump_project(const project_t &p);

private:
    explicit project_table();
    ~project_table();
};
}  // namespace csp

namespace YAML {
template <> struct convert<csp::project_table::project_t>
{
    static Node encode(const csp::project_table::project_t &rhs)
    {
        Node node;
        node.force_insert("Core", rhs.core);
        return node;
    }

    static bool decode(const Node &node, csp::project_table::project_t &rhs)
    {
        if (!node.IsMap() || node.size() != 1)
            return false;

        rhs.core = node["Core"].as<QMap<QString, QString>>();
        return true;
    }
};
}  // namespace YAML

#endif  // COMMON_PROJECT_CSP_PROJECT_TABLE_H
