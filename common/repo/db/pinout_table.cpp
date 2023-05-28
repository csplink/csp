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

using namespace csp;

pinout_table::pinout_table() = default;

pinout_table::~pinout_table() = default;

pinout_table::pinout_t pinout_table::load_pinout(const QString &path)
{
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        std::string buffer;
        QFile       file(path);

        file.open(QFileDevice::ReadOnly | QIODevice::Text);
        buffer = file.readAll().toStdString();
        file.close();
        YAML::Node yaml_data = YAML::Load(buffer);
        return yaml_data.as<pinout_table::pinout_t>();
    }
    catch (YAML::BadFile &e)
    {
        os::show_error_and_exit(e.what());
        throw;
    }
    catch (YAML::BadConversion &e)
    {
        os::show_error_and_exit(e.what());
        throw;
    }
    catch (std::exception &e)
    {
        qDebug() << e.what();
        throw;
    }

    return {};
}
