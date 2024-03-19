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
#include "os.h"
#include "qtjson.h"
#include "qtyaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::document_t, url)
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::module_t, description)
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::mdk_arm_t, device, packs, pack_url, cmsis_core)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(chip_summary_table::target_project_t, xmake, cmake, mdk_arm)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(chip_summary_table::linker_t, default_minimum_heap_size,
                                            default_minimum_stack_size)
YAML_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::chip_summary_t, clocktree, company, company_url, documents, hal,
                               has_powerpad, illustrate, introduction, line, modules, name, package, series, url,
                               target_project, linker)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::document_t, url)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::module_t, description)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::mdk_arm_t, device, packs, pack_url, cmsis_core)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::target_project_t, xmake, cmake, mdk_arm)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::linker_t, default_minimum_heap_size, default_minimum_stack_size)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(chip_summary_table::chip_summary_t, clocktree, company, company_url, documents, hal,
                                   has_powerpad, illustrate, introduction, line, modules, name, package, series, url,
                                   target_project, linker)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(chip_summary_table::document_t)
QT_DEBUG_ADD_TYPE(chip_summary_table::module_t)
QT_DEBUG_ADD_TYPE(chip_summary_table::mdk_arm_t)
QT_DEBUG_ADD_TYPE(chip_summary_table::target_project_t)
QT_DEBUG_ADD_TYPE(chip_summary_table::chip_summary_t)

chip_summary_table::chip_summary_table() = default;

chip_summary_table::~chip_summary_table() = default;

void chip_summary_table::load_chip_summary(chip_summary_t *chip_summary, const QString &path)
{
    Q_ASSERT(chip_summary != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    static const QRegularExpression pattern("^0x[0-9a-fA-F]+$");

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const YAML::Node yaml_data = YAML::Load(buffer);
        YAML::convert<chip_summary_t>::decode(yaml_data, *chip_summary);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }

    if (!chip_summary->linker.default_minimum_heap_size.isEmpty())
    {
        if (!pattern.match(chip_summary->linker.default_minimum_heap_size).hasMatch())
        {
            qWarning() << QObject::tr("The field chip_summary_t::linker_t::default_minimum_heap_size is an "
                                      "illegal value %1, and the default value 0x200 is used.")
                              .arg(chip_summary->linker.default_minimum_heap_size);
            chip_summary->linker.default_minimum_heap_size = "0x200";
        }
    }

    if (!chip_summary->linker.default_minimum_stack_size.isEmpty())
    {
        if (!pattern.match(chip_summary->linker.default_minimum_stack_size).hasMatch())
        {
            qWarning() << QObject::tr("The field chip_summary_t::linker_t::default_minimum_stack_size is an "
                                      "illegal value %1, and the default value 0x400 is used.")
                              .arg(chip_summary->linker.default_minimum_stack_size);
            chip_summary->linker.default_minimum_stack_size = "0x400";
        }
    }
}

void chip_summary_table::load_chip_summary(chip_summary_t *chip_summary, const QString &company, const QString &name)
{
    Q_ASSERT(chip_summary != nullptr);
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    const QString path = QString("%1/db/chips/%2/%3.yml").arg(Config::repoDir(), company.toLower(), name.toLower());
    return load_chip_summary(chip_summary, path);
}
