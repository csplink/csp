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

#include <QFile>
#include <QRegularExpression>

#include "ChipSummaryTable.h"
#include "QtJson.h"
#include "QtYaml.h"
#include "Settings.h"
#include "Utils.h"

namespace QT_YAML
{
QT_YAML_GEN_PARSE_CODE(ChipSummaryTable::DocumentType, Url)
QT_YAML_GEN_PARSE_CODE(ChipSummaryTable::ModuleType, Description)
QT_YAML_GEN_PARSE_CODE(ChipSummaryTable::MdkArmType, Versions)

#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {"MdkArm"};
QT_YAML_GEN_PARSE_CODE(ChipSummaryTable::TargetProjectType, XMake, CMake, MdkArm)
#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {};

QT_YAML_GEN_PARSE_CODE(ChipSummaryTable::LinkerType, DefaultHeapSize, DefaultStackSize)
QT_YAML_GEN_PARSE_CODE(ChipSummaryTable::ChipSummaryType, ClockTree, Vendor, VendorUrl, Documents, Hal, HasPowerPad,
                       Illustrate, Introduction, Line, Modules, Name, Package, Series, Url, TargetProject, Toolchains,
                       Linker)
} // namespace QT_YAML

namespace QT_JSON
{
QT_JSON_GEN_PARSE_CODE(ChipSummaryTable::DocumentType, Url)
QT_JSON_GEN_PARSE_CODE(ChipSummaryTable::ModuleType, Description)
QT_JSON_GEN_PARSE_CODE(ChipSummaryTable::MdkArmType, Versions)
QT_JSON_GEN_PARSE_CODE(ChipSummaryTable::TargetProjectType, XMake, CMake, MdkArm)
QT_JSON_GEN_PARSE_CODE(ChipSummaryTable::LinkerType, DefaultHeapSize, DefaultStackSize)

#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {"Linker"};
QT_JSON_GEN_PARSE_CODE(ChipSummaryTable::ChipSummaryType, ClockTree, Vendor, VendorUrl, Documents, Hal, HasPowerPad,
                       Illustrate, Introduction, Line, Modules, Name, Package, Series, Url, TargetProject, Linker)
#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {};
} // namespace QT_JSON

QT_DEBUG_ADD_TYPE(ChipSummaryTable::DocumentType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::ModuleType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::MdkArmType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::TargetProjectType)
QT_DEBUG_ADD_TYPE(ChipSummaryTable::ChipSummaryType)

ChipSummaryTable::ChipSummaryTable() = default;

ChipSummaryTable::~ChipSummaryTable() = default;

bool ChipSummaryTable::loadChipSummary(ChipSummaryType *chipSummary, const QString &path)
{
    bool rtn = false;
    if (chipSummary != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<ChipSummaryType>::decode(yaml_data, *chipSummary);
                rtn = true;
            }
            catch (std::exception &e)
            {
                const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
                qCritical().noquote() << str;
                throw;
            }

            file.close();

            if (!chipSummary->Linker.DefaultHeapSize.isEmpty() && !Utils::isHex(chipSummary->Linker.DefaultHeapSize))
            {
                qWarning().noquote() << QObject::tr("The field ChipSummaryType::LinkerType::DefaultHeapSize is an "
                                                    "illegal value %1, and the default value 0x200 is used.")
                                            .arg(chipSummary->Linker.DefaultHeapSize);
                chipSummary->Linker.DefaultHeapSize = "0x200";
            }

            if (!chipSummary->Linker.DefaultStackSize.isEmpty() && !Utils::isHex(chipSummary->Linker.DefaultStackSize))
            {
                qWarning().noquote() << QObject::tr("The field ChipSummaryType::LinkerType::DefaultStackSize is an "
                                                    "illegal value %1, and the default value 0x400 is used.")
                                            .arg(chipSummary->Linker.DefaultStackSize);
                chipSummary->Linker.DefaultStackSize = "0x400";
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
    return rtn;
}

bool ChipSummaryTable::loadChipSummary(ChipSummaryType *chipSummary, const QString &vendor, const QString &name)
{
    bool rtn = false;
    if (chipSummary != nullptr)
    {
        if (!vendor.isEmpty() && !name.isEmpty())
        {
            const QString path = QString("%1/chips/%2/%3.yml").arg(Settings.database(), vendor, name);
            rtn = loadChipSummary(chipSummary, path);
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
    return rtn;
}

bool ChipSummaryTable::fileExists(const QString &vendor, const QString &name)
{
    return QFile::exists(QString("%1/chips/%2/%3.yml").arg(Settings.database(), vendor, name));
}
