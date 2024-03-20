/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ProjectTable.h
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

#ifndef CSP_PROJECT_PROJECT_TABLE_H
#define CSP_PROJECT_PROJECT_TABLE_H

#include <QMap>

class ProjectTable
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
    } PinConfigType;

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
    } CoreType;

    typedef struct mdk_arm_struct
    {
        QString device;     // pack 中的名字
        QString pack;       // pack
        QString pack_url;   // cmsis pack更新url
        QString cmsis_core; // 依赖的cmsis core最低版本
    } MdkArmType;

    typedef struct target_project_struct
    {
        MdkArmType mdk_arm;
    } TargetProjectType;

    typedef struct
    {
        QString name;                            // project name
        QString version;                         // csp version
        QString target;                          // target type: xmake, mdk, cmake
        QMap<QString, PinConfigType> pin_configs; // pin configs
        CoreType core;                            // core configs
        TargetProjectType target_project;
    } ProjectType;

  public:
    /**
     * @brief load project from json file
     * @param project: project ptr
     * @param path: project file path
     * @return void
     */
    static void loadProject(ProjectType *project, const QString &path);

    /**
     * @brief save project to json file
     * @param project: project
     * @param path: project file path
     */
    static void saveProject(ProjectType &project, const QString &path);

    /**
     * @brief dump project to json string
     * @param project: project
     * @return yaml string
     */
    static QString dumpProject(ProjectType &project);

  private:
    explicit ProjectTable();
    ~ProjectTable();

    static void setValue(ProjectType &project);
};

#endif /** CSP_PROJECT_PROJECT_TABLE_H */
