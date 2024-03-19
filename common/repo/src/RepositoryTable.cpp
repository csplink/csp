/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        RepositoryTable.cpp
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
 *  2023-04-20     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>

#include "RepositoryTable.h"
#include "os.h"
#include "qtjson.h"
#include "qtyaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::CurrentType, lowest, run)
YAML_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::TemperatureType, max, min)
YAML_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::VoltageType, max, min)
YAML_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::ChipInfoType, core, current, flash, frequency, io, package, peripherals,
                               ram, temperature, voltage)
YAML_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::RepositoryType, chips)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::CurrentType, lowest, run)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::TemperatureType, max, min)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::VoltageType, max, min)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::ChipInfoType, core, current, flash, frequency, io, package,
                                   peripherals, ram, temperature, voltage)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(RepositoryTable::RepositoryType, chips)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(RepositoryTable::CurrentType)
QT_DEBUG_ADD_TYPE(RepositoryTable::TemperatureType)
QT_DEBUG_ADD_TYPE(RepositoryTable::VoltageType)
QT_DEBUG_ADD_TYPE(RepositoryTable::ChipInfoType)
QT_DEBUG_ADD_TYPE(RepositoryTable::RepositoryType)

RepositoryTable::RepositoryTable() = default;

void RepositoryTable::loadRepository(RepositoryType *repository, const QString &path)
{
    Q_ASSERT(repository != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const YAML::Node yaml_data = YAML::Load(buffer);
        YAML::convert<RepositoryType>::decode(yaml_data, *repository);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

RepositoryTable::~RepositoryTable() = default;
