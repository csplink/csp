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

#include <QDebug>
#include <QMap>

class ProjectTable
{
  public:
    typedef QMap<QString, QString> PinFunctionPropertyType;
    typedef QMap<QString, PinFunctionPropertyType> PinFunctionPropertiesType;

    typedef struct
    {
        QString Function;                           // pin selected function
        QString Comment;                            // pin comment
        bool Locked;                                // pin locked
        PinFunctionPropertiesType FunctionProperty; // pin function properties
    } PinConfigType;

    typedef struct
    {
        QString Device;    // pack 中的名字
        QString Pack;      // pack
        QString PackUrl;   // cmsis pack更新url
        QString CmsisCore; // 依赖的cmsis core最低版本
    } MdkArmType;

    typedef struct
    {
        MdkArmType MdkArm;
    } TargetProjectType;

    typedef struct
    {
        QString Company;                         // company
        QString Hal;                             // hal
        QString HalVersion;                      // hal version
        QStringList Modules;                     // modules
        QString Package;                         // package
        QString TargetChip;                      // target
        QString Toolchains;                      // toolchains
        QString ToolchainsVersion;               // toolchains version
        QString Type;                            // type
        QString Name;                            // project name
        QMap<QString, PinConfigType> PinConfigs; // pin configs
        QString TargetProject;                   // target project type: xmake, mdk, cmake
        TargetProjectType TargetProjectConfig;   // target Project config
        QString Version;                         // csp version
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

QDebug operator<<(QDebug, const ProjectTable::PinConfigType &);
QDebug operator<<(QDebug, const ProjectTable::MdkArmType &);
QDebug operator<<(QDebug, const ProjectTable::TargetProjectType &);
QDebug operator<<(QDebug, const ProjectTable::ProjectType &);

#endif /** CSP_PROJECT_PROJECT_TABLE_H */
