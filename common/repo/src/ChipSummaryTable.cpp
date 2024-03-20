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
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::DocumentType, url)
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ModuleType, description)
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::MdkArmType, device, packs, pack_url, cmsis_core)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ChipSummaryTable::TargetProjectType, xmake, cmake, mdk_arm)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(ChipSummaryTable::LinkerType, default_minimum_heap_size,
                                            default_minimum_stack_size)
YAML_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ChipSummaryType, clocktree, company, company_url, documents, hal,
                               has_powerpad, illustrate, introduction, line, modules, name, package, series, url,
                               target_project, linker)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::DocumentType, url)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ModuleType, description)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::MdkArmType, device, packs, pack_url, cmsis_core)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::TargetProjectType, xmake, cmake, mdk_arm)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::LinkerType, default_minimum_heap_size, default_minimum_stack_size)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(ChipSummaryTable::ChipSummaryType, clocktree, company, company_url, documents, hal,
                                   has_powerpad, illustrate, introduction, line, modules, name, package, series, url,
                                   target_project, linker)
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

            if (!chipSummary->linker.default_minimum_heap_size.isEmpty())
            {
                if (!pattern.match(chipSummary->linker.default_minimum_heap_size).hasMatch())
                {
                    qWarning().noquote() << QObject::tr("The field chip_summary_t::linker_t::default_minimum_heap_size is an "
                                                        "illegal value %1, and the default value 0x200 is used.")
                                                .arg(chipSummary->linker.default_minimum_heap_size);
                    chipSummary->linker.default_minimum_heap_size = "0x200";
                }
            }

            if (!chipSummary->linker.default_minimum_stack_size.isEmpty())
            {
                if (!pattern.match(chipSummary->linker.default_minimum_stack_size).hasMatch())
                {
                    qWarning().noquote() << QObject::tr("The field chip_summary_t::linker_t::default_minimum_stack_size is an "
                                                        "illegal value %1, and the default value 0x400 is used.")
                                                .arg(chipSummary->linker.default_minimum_stack_size);
                    chipSummary->linker.default_minimum_stack_size = "0x400";
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
