/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PinoutTable.cpp
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
 *  2023-05-28     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>

#include "Config.h"
#include "PinoutTable.h"
#include "QtJson.h"
#include "QtYaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(PinoutTable::FunctionType, Mode, Type)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(PinoutTable::PinoutUnitType, Position, Type, Functions)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(PinoutTable::FunctionType, Mode, Type)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(PinoutTable::PinoutUnitType, Position, Type, Functions)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(PinoutTable::FunctionType)
QT_DEBUG_ADD_TYPE(PinoutTable::PinoutUnitType)

PinoutTable::PinoutTable() = default;

PinoutTable::~PinoutTable() = default;

void PinoutTable::loadPinout(PinoutType *pinout, const QString &company, const QString &hal, const QString &name)
{
    if (pinout != nullptr)
    {
        if (!hal.isEmpty() && !name.isEmpty())
        {
            const QString path = QString("%1/db/hal/%2/%3/%4/pinout.yml").arg(Config::repoDir(), company.toLower(), hal.toLower(), name.toLower());
            loadPinout(pinout, path);
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

void PinoutTable::loadPinout(PinoutType *pinout, const QString &path)
{
    if (pinout != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<PinoutType>::decode(yaml_data, *pinout);
            }
            catch (std::exception &e)
            {
                const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
                qCritical().noquote() << str;
                throw;
            }

            file.close();

            if (!pinout->isEmpty())
            {
                auto pinout_i = pinout->constBegin();
                while (pinout_i != pinout->constEnd())
                {
                    const QString &key = pinout_i.key();
                    const PinoutUnitType &unit = pinout_i.value();
                    const int &position = unit.Position;
                    const QString &type = unit.Type;
                    const QMap<QString, FunctionType> &functions = pinout_i.value().Functions;
                    if (position > 0 && !type.isEmpty())
                    {
                        if (type.toLower() == "i/o")
                        {
                            if (functions.isEmpty())
                            {
                                qCritical().noquote() << QString("%1: pinout %2`s functions is empty").arg(path, key);
                                /** TODO: error */
                            }
                        }
                        else if (type.toLower() == "power" || type.toLower() == "nc" || type.toLower() == "boot" ||
                                 type.toLower() == "reset")
                        { /* do nothings */
                        }
                        else
                        {
                            qCritical().noquote() << QString("%1: pinout %2`s type<%3> is invalid").arg(path, key, type);
                            /** TODO: error */
                        }

                        ++pinout_i;
                    }
                    else
                    {
                        /** TODO: QString("%1: pinout %2`s position<%3> is invalid").arg(path, key).arg(position);
                         *        QString("%1: pinout %2`s type is empty").arg(path, key);
                         */
                    }
                }
            }
            else
            {
                /** TODO: path + ": pinout is empty" */
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
