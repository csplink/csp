/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        chip_summary_table.cpp
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

#include "chip_summary_table.h"
#include "config.h"
#include "os.h"

using namespace csp;

chip_summary_table::chip_summary_table() = default;

chip_summary_table::~chip_summary_table() = default;

chip_summary_table::chip_summary_t chip_summary_table::load_chip_summary(const QString &path)
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
        return yaml_data.as<chip_summary_table::chip_summary_t>();
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

chip_summary_table::chip_summary_t chip_summary_table::load_chip_summary(const QString &company, const QString &name)
{
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    QString path = QString("%1/db/chips/%2/%3.yml").arg(config::repodir(), company.toLower(), name.toLower());
    return load_chip_summary(path);
}
