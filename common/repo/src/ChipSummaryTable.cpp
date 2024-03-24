/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ChipSummaryTable.cpp
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

#include <QDebug>
#include <QFile>
#include <QRegularExpression>

#include "ChipSummaryTable.h"
#include "Config.h"
#include "QtJson.h"
#include "QtYaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::DocumentType, Url)
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ModuleType, Description)
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::MdkArmType, Device, Packs, PackUrl, CmsisCore)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ChipSummaryTable::TargetProjectType, XMake, CMake, MdkArm)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ChipSummaryTable::LinkerType, DefaultMinimumHeapSize,
                                            DefaultMinimumStackSize)
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ChipSummaryType, ClockTree, Company, CompanyUrl, Documents, Hal,
                               HasPowerPad, Illustrate, Introduction, Line, Modules, Name, Package, Series, Url,
                               TargetProject, Linker)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::DocumentType, Url)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ModuleType, Description)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::MdkArmType, Device, Packs, PackUrl, CmsisCore)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::TargetProjectType, XMake, CMake, MdkArm)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::LinkerType, DefaultMinimumHeapSize, DefaultMinimumStackSize)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ChipSummaryType, ClockTree, Company, CompanyUrl, Documents, Hal,
                                   HasPowerPad, Illustrate, Introduction, Line, Modules, Name, Package, Series, Url,
                                   TargetProject, Linker)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(ChipSummaryTable::DocumentType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::ModuleType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::MdkArmType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::TargetProjectType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::ChipSummaryType)

ChipSummaryTable::ChipSummaryTable() = default;

ChipSummaryTable::~ChipSummaryTable() = default;

void ChipSummaryTable::loadChipSummary(ChipSummaryType *chipSummary, const QString &path)
{
    if (chipSummary != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            static const QRegularExpression pattern("^0x[0-9a-fA-F]+$");
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<ChipSummaryType>::decode(yaml_data, *chipSummary);
            }
            catch (std::exception &e)
            {
                const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
                qCritical().noquote() << str;
                throw;
            }

            file.close();

            if (!chipSummary->Linker.DefaultMinimumHeapSize.isEmpty())
            {
                if (!pattern.match(chipSummary->Linker.DefaultMinimumHeapSize).hasMatch())
                {
                    qWarning().noquote() << QObject::tr("The field chip_summary_t::linker_t::default_minimum_heap_size is an "
                                                        "illegal value %1, and the default value 0x200 is used.")
                                                .arg(chipSummary->Linker.DefaultMinimumHeapSize);
                    chipSummary->Linker.DefaultMinimumHeapSize = "0x200";
                }
            }

            if (!chipSummary->Linker.DefaultMinimumStackSize.isEmpty())
            {
                if (!pattern.match(chipSummary->Linker.DefaultMinimumStackSize).hasMatch())
                {
                    qWarning().noquote() << QObject::tr("The field chip_summary_t::linker_t::default_minimum_stack_size is an "
                                                        "illegal value %1, and the default value 0x400 is used.")
                                                .arg(chipSummary->Linker.DefaultMinimumStackSize);
                    chipSummary->Linker.DefaultMinimumStackSize = "0x400";
                }
            }
        }
        else
        {
            /** TODO: failed */
        }
    }
    else
    {
        /** TODO: failed */
    }
}

void ChipSummaryTable::loadChipSummary(ChipSummaryType *chipSummary, const QString &company, const QString &name)
{
    if (chipSummary != nullptr)
    {
        if (!company.isEmpty() && !name.isEmpty())
        {
            const QString path = QString("%1/db/chips/%2/%3.yml").arg(Config::repoDir(), company.toLower(), name.toLower());
            loadChipSummary(chipSummary, path);
        }
        else
        {
            /** TODO: failed */
        }
    }
    else
    {
        /** TODO: failed */
    }
}
