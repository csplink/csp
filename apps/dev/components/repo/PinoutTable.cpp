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

#include <QFile>

#include "PinoutTable.h"
#include "QtJson.h"
#include "QtYaml.h"
#include "Settings.h"

namespace QT_YAML
{
#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {"Mode", "Type"};
QT_YAML_GEN_PARSE_CODE(PinoutTable::FunctionType, Mode, Type)

#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {"Functions"};
QT_YAML_GEN_PARSE_CODE(PinoutTable::PinoutUnitType, Position, Type, Functions)
#undef QT_YAML_MAYBE_UNUSED_LIST
#define QT_YAML_MAYBE_UNUSED_LIST {};
} // namespace QT_YAML

namespace QT_JSON
{
QT_JSON_GEN_PARSE_CODE(PinoutTable::FunctionType, Mode, Type)
QT_JSON_GEN_PARSE_CODE(PinoutTable::PinoutUnitType, Position, Type, Functions)
} // namespace QT_JSON

QT_DEBUG_ADD_TYPE(PinoutTable::FunctionType)
QT_DEBUG_ADD_TYPE(PinoutTable::PinoutUnitType)

PinoutTable::PinoutTable() = default;

PinoutTable::~PinoutTable() = default;

bool PinoutTable::loadPinout(PinoutType *pinout, const QString &vendor, const QString &hal, const QString &name)
{
    bool rtn = false;
    if (pinout != nullptr)
    {
        if (!hal.isEmpty() && !name.isEmpty())
        {
            const QString path = QString("%1/hal/%2/%3/%4/pinout.yml").arg(Settings.database(), vendor, hal, name);
            rtn = loadPinout(pinout, path);
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

bool PinoutTable::loadPinout(PinoutType *pinout, const QString &path)
{
    bool rtn = false;
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
                rtn = true;
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
                        if (type == "I/O")
                        {
                            if (functions.isEmpty())
                            {
                                qCritical().noquote() << QString("%1: pinout %2`s functions is empty").arg(path, key);
                                /** TODO: error */
                            }
                        }
                        else if (type == "Power" || type == "NC" || type == "Boot" || type == "Reset")
                        { /* do nothings */
                        }
                        else
                        {
                            qCritical().noquote()
                                << QString("%1: pinout %2`s type<%3> is invalid").arg(path, key, type);
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
    return rtn;
}
