/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ChipSummaryTable.h
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
 *  2023-05-21     xqyjlj       initial version
 */

#ifndef CSP_REPO_CHIP_SUMMARY_TABLE_H
#define CSP_REPO_CHIP_SUMMARY_TABLE_H

#include <QMap>

class ChipSummaryTable final
{
  public:
    typedef struct
    {
        QMap<QString, QString> url;
    } DocumentType;

    typedef struct
    {
        QMap<QString, QString> description;
    } ModuleType;

    typedef QMap<QString, QMap<QString, DocumentType>> DocumentsType;
    typedef QMap<QString, QMap<QString, ModuleType>> ModulesType;

    typedef struct
    {
        QString device;     // pack 中的名字
        QStringList packs;  // pack 列表
        QString pack_url;   // cmsis pack更新url
        QString cmsis_core; // 依赖的cmsis core最低版本
    } MdkArmType;

    typedef struct
    {
        bool xmake;
        bool cmake;
        MdkArmType mdk_arm;
    } TargetProjectType;

    typedef struct
    {
        QString default_minimum_heap_size;
        QString default_minimum_stack_size;
    } LinkerType;

    typedef struct
    {
        QString clocktree;
        QString company;
        QMap<QString, QString> company_url;
        DocumentsType documents;
        QString hal;
        bool has_powerpad;
        QMap<QString, QString> illustrate;
        QMap<QString, QString> introduction;
        QString line;
        ModulesType modules;
        QString name;
        QString package;
        QString series;
        QMap<QString, QString> url;
        TargetProjectType target_project;
        LinkerType linker;
    } ChipSummaryType;

    static void loadChipSummary(ChipSummaryType *chipSummary, const QString &path);
    static void loadChipSummary(ChipSummaryType *chipSummary, const QString &company, const QString &name);

  private:
    explicit ChipSummaryTable();
    ~ChipSummaryTable();
};

#endif /** CSP_REPO_CHIP_SUMMARY_TABLE_H */
