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

#ifndef __CHIP_SUMMARY_TABLE_H__
#define __CHIP_SUMMARY_TABLE_H__

#include <QDebug>
#include <QMap>

class ChipSummaryTable final
{
  public:
    typedef struct
    {
        QMap<QString, QString> Url;
    } DocumentType;

    typedef struct
    {
        QMap<QString, QString> Description;
    } ModuleType;

    typedef QMap<QString, QMap<QString, DocumentType>> DocumentsType;
    typedef QMap<QString, QMap<QString, ModuleType>> ModulesType;

    typedef struct
    {
        QStringList Versions;
    } MdkArmType;

    typedef struct
    {
        bool XMake;
        bool CMake;
        MdkArmType MdkArm;
    } TargetProjectType;

    typedef struct
    {
        QString DefaultHeapSize;
        QString DefaultStackSize;
    } LinkerType;

    typedef struct
    {
        QString ClockTree;
        QString Company;
        QMap<QString, QString> CompanyUrl;
        DocumentsType Documents;
        QString Hal;
        bool HasPowerPad;
        QMap<QString, QString> Illustrate;
        QMap<QString, QString> Introduction;
        QString Line;
        ModulesType Modules;
        QString Name;
        QString Package;
        QString Series;
        QMap<QString, QString> Url;
        TargetProjectType TargetProject;
        QString Toolchains;
        LinkerType Linker;
    } ChipSummaryType;

    static bool loadChipSummary(ChipSummaryType *chipSummary, const QString &path);
    static bool loadChipSummary(ChipSummaryType *chipSummary, const QString &company, const QString &name);
    static bool fileExists(const QString &company, const QString &name);

  private:
    explicit ChipSummaryTable();
    ~ChipSummaryTable();
};

QDebug operator<<(QDebug, const ChipSummaryTable::DocumentType &);
QDebug operator<<(QDebug, const ChipSummaryTable::ModuleType &);
QDebug operator<<(QDebug, const ChipSummaryTable::MdkArmType &);
QDebug operator<<(QDebug, const ChipSummaryTable::TargetProjectType &);
QDebug operator<<(QDebug, const ChipSummaryTable::ChipSummaryType &);

#endif /** __CHIP_SUMMARY_TABLE_H__ */
