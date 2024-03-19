/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        IpTable.cpp
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
#include <QFileInfo>

#include "Config.h"
#include "IpTable.h"
#include "os.h"
#include "qtjson.h"
#include "qtyaml.h"

QT_DEBUG_ADD_TYPE(IpTable::IpMapType)
QT_DEBUG_ADD_TYPE(IpTable::IpType)
QT_DEBUG_ADD_TYPE(IpTable::IpsType)

IpTable::IpTable() = default;

IpTable::~IpTable() = default;

void IpTable::loadIp(IpType *ip, const QString &path)
{
    Q_ASSERT(ip != nullptr);
    Q_ASSERT(!path.isEmpty());
    Q_ASSERT(os::isfile(path));

    try
    {
        const std::string buffer = os::readfile(path).toStdString();
        const YAML::Node yaml_data = YAML::Load(buffer);
        YAML::convert<IpType>::decode(yaml_data, *ip);
    }
    catch (std::exception &e)
    {
        const QString str = QString("try to parse file \"%1\" failed. \n\nreason: %2").arg(path, e.what());
        qCritical().noquote() << str;
        os::show_error_and_exit(str);
        throw;
    }
}

void IpTable::loadIp(IpType *ip, const QString &hal, const QString &name, const QString &ipName)
{
    Q_ASSERT(ip != nullptr);
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());
    Q_ASSERT(!ipName.isEmpty());

    const QString path =
        QString("%1/db/hal/%2/%3/ip/%4.yml").arg(Config::repoDir(), hal.toLower(), name.toLower(), ipName.toLower());
    return loadIp(ip, path);
}

void IpTable::loadIps(IpsType *ips, const QString &hal, const QString &name)
{
    Q_ASSERT(ips != nullptr);
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!name.isEmpty());

    const QString path = QString("%1/db/hal/%2/%3/ip").arg(Config::repoDir(), hal.toLower(), name.toLower());
    for (const QString &file : os::files(path, QString("*.yml")))
    {
        IpType ip;
        loadIp(&ip, file);
        const QFileInfo info(file);
        auto basename = info.baseName().toLower();
        ips->insert(basename, ip);
    }

    const QStringList list = { "gpio" };
    for (const QString &file : list)
    {
        IpType ip;
        loadIp(&ip, QString(":/lib/repo/db/ip/%1.yml").arg(file));
        const QFileInfo info(file);
        const QString basename = info.baseName().toLower();
        if (ips->contains(basename))
        {
            IpType &ref_ip = (*ips)[basename];
            auto ip_i = ip.constBegin();
            while (ip_i != ip.constEnd())
            {
                ref_ip.insert(ip_i.key(), ip_i.value());
                ++ip_i;
            }
        }
        else
        {
            ips->insert(basename, ip);
        }
    }
}
