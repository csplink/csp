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

#include <QMap>

class project_table
{
  public:
    typedef QMap<QString, QString> pin_function_property_t;
    typedef QMap<QString, pin_function_property_t> pin_function_properties_t;

    typedef struct
    {
        QString function;                            // pin selected function
        QString comment;                             // pin comment
        bool locked;                                 // pin locked
        pin_function_properties_t function_property; // pin function properties
    } pin_config_t;

    typedef struct
    {
        QString hal;           // hal
        QString target;        // target
        QString package;       // package
        QString company;       // company
        QString type;          // type
        QString toolchains;    // toolchains
        QStringList modules;   // modules
        QStringList warnings;  // warnings
        QStringList languages; // languages
    } core_t;

    typedef struct
    {
        QString name;                            // project name
        QString version;                         // csp version
        QString target;                          // target type: xmake, mdk, cmake
        QMap<QString, pin_config_t> pin_configs; // pin configs
        core_t core;                             // core configs
    } project_t;

  public:
    /**
     * @brief load project from json file
     * @param proj: project ptr
     * @param path: project file path
     * @return void
     */
    static void load_project(project_t *proj, const QString &path);

    /**
     * @brief save project to json file
     * @param p: project
     * @param path: project file path
     */
    static void save_project(project_t &p, const QString &path);

    /**
     * @brief dump project to json string
     * @param p: project
     * @return yaml string
     */
    static QString dump_project(project_t &proj);

  private:
    explicit project_table();
    ~project_table();

    static void set_value(project_t &proj);
};

#endif // COMMON_PROJECT_CSP_PROJECT_TABLE_H
