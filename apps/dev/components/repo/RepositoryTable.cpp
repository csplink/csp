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

#include <QFile>

#include "QtJson.h"
#include "QtYaml.h"
#include "RepositoryTable.h"

namespace QT_YAML
{
QT_YAML_GEN_PARSE_CODE(RepositoryTable::CurrentType, Lowest, Run)
QT_YAML_GEN_PARSE_CODE(RepositoryTable::TemperatureType, Max, Min)
QT_YAML_GEN_PARSE_CODE(RepositoryTable::VoltageType, Max, Min)
QT_YAML_GEN_PARSE_CODE(RepositoryTable::ChipInfoType, Core, Current, Flash, Frequency, IO, Package, Peripherals, Ram,
                       Temperature, Voltage)
QT_YAML_GEN_PARSE_CODE(RepositoryTable::RepositoryType, Chips)
} // namespace QT_YAML

namespace QT_JSON
{
QT_JSON_GEN_PARSE_CODE(RepositoryTable::CurrentType, Lowest, Run)
QT_JSON_GEN_PARSE_CODE(RepositoryTable::TemperatureType, Max, Min)
QT_JSON_GEN_PARSE_CODE(RepositoryTable::VoltageType, Max, Min)
QT_JSON_GEN_PARSE_CODE(RepositoryTable::ChipInfoType, Core, Current, Flash, Frequency, IO, Package, Peripherals, Ram,
                       Temperature, Voltage)
QT_JSON_GEN_PARSE_CODE(RepositoryTable::RepositoryType, Chips)
} // namespace QT_JSON

QT_DEBUG_ADD_TYPE(RepositoryTable::CurrentType)
QT_DEBUG_ADD_TYPE(RepositoryTable::TemperatureType)
QT_DEBUG_ADD_TYPE(RepositoryTable::VoltageType)
QT_DEBUG_ADD_TYPE(RepositoryTable::ChipInfoType)
QT_DEBUG_ADD_TYPE(RepositoryTable::RepositoryType)

RepositoryTable::RepositoryTable() = default;

bool RepositoryTable::loadRepository(RepositoryType *repository, const QString &path)
{
    bool rtn = false;
    if (repository != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<RepositoryType>::decode(yaml_data, *repository);
                rtn = true;
            }
            catch (std::exception &e)
            {
                const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
                qCritical().noquote() << str;
                throw;
            }

            file.close();
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

RepositoryTable::~RepositoryTable() = default;
