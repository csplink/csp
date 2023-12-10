/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        pinout_table.cpp
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

#include "config.h"
#include "os.h"
#include "pinout_table.h"
#include "qtjson.h"
#include "qtyaml.h"

namespace YAML
{
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(pinout_table::function_t, mode, type)
YAML_DEFINE_TYPE_NON_INTRUSIVE_MAYBE_UNUSED(pinout_table::pinout_unit_t, position, type, functions)
} // namespace YAML

namespace nlohmann
{
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(pinout_table::function_t, mode, type)
NLOHMANN_DEFINE_TYPE_NON_INTRUSIVE(pinout_table::pinout_unit_t, position, type, functions)
} // namespace nlohmann

QT_DEBUG_ADD_TYPE(pinout_table::function_t)
QT_DEBUG_ADD_TYPE(pinout_table::pinout_unit_t)

pinout_table::pinout_table() = default;

pinout_table::~pinout_table() = default;

void pinout_table::load_pinout(pinout_t *pinout, const QString &hal, const QString &name)
{
    Q_ASSERT(pinout != nullptr);
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());

    const QString path = QString("%1/db/hal/%2/%3/pinout.yml").arg(config::repodir(), hal.toLower(), name.toLower());
    load_pinout(pinout, path);
}

void pinout_table::load_pinout(pinout_t *pinout, const QString &path)
{
    Q_ASSERT(pinout != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const YAML::Node yaml_data = YAML::Load(buffer);
        YAML::convert<pinout_t>::decode(yaml_data, *pinout);

        os_assert(!pinout->isEmpty(), path + ": pinout is empty");

        auto pinou_i = pinout->constBegin();
        while (pinou_i != pinout->constEnd())
        {
            const QString &key = pinou_i.key();
            const pinout_unit_t &unit = pinou_i.value();
            const int &position = unit.position;
            const QString &type = unit.type;
            const QMap<QString, function_t> &functions = pinou_i.value().functions;
            os_assert(!key.isEmpty(), path + ": pinout key is empty");
            os_assert(position > 0, QString("%1: pinout %2`s position<%3> is invalid").arg(path, key).arg(position));
            os_assert(!type.isEmpty(), QString("%1: pinout %2`s type is empty").arg(path, key));

            if (type.toLower() == "i/o")
            {
                os_assert(!functions.isEmpty(), QString("%1: pinout %2`s functions is empty").arg(path, key));
            }
            else if (type.toLower() == "power" || type.toLower() == "nc" || type.toLower() == "boot" ||
                     type.toLower() == "reset")
            {
                /* do nothings */
            }
            else
            {
                os_assert(0, QString("%1: pinout %2`s type<%3> is invalid").arg(path, key, type));
            }

            ++pinou_i;
        }
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }
}
