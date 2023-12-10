/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ip_table.cpp
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
 *  2023-06-16     xqyjlj       initial version
 */

#include <QDebug>
#include <QFile>

#include "config.h"
#include "ip_table.h"
#include "os.h"
#include "path.h"

ip_table::ip_table() = default;

ip_table::~ip_table() = default;

ip_table::ip_t ip_table::load_ip(const QString &path)
{
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        QFile file(path);

        file.open(QFileDevice::ReadOnly | QIODevice::Text);
        const std::string buffer = file.readAll().toStdString();
        file.close();
        const YAML::Node yaml_data = YAML::Load(buffer);
        return yaml_data.as<ip_table::ip_t>();
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

QMap<QString, ip_table::ip_map_t> ip_table::load_ip(const QString &hal, const QString &name, const QString &ip)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());
    Q_ASSERT(!ip.isEmpty());

    const QString path =
        QString("%1/db/hal/%2/%3/ip/%4.yml").arg(config::repodir(), hal.toLower(), name.toLower(), ip.toLower());
    return load_ip(path);
}

ip_table::ips_t ip_table::load_ips(const QString &hal, const QString &name)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());

    QMap<QString, ip_table::ip_t> ips;
    const QString path = QString("%1/db/hal/%2/%3/ip").arg(config::repodir(), hal.toLower(), name.toLower());
    for (const QString &file : os::files(path, QString("*.yml")))
    {
        auto ip = load_ip(file);
        auto basename = path::basename(file).toLower();
        ips.insert(basename, ip);
    }
    return ips;
}
