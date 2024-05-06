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

#include <QDir>
#include <QFile>
#include <QFileInfo>

#include "IpTable.h"
#include "QtJson.h"
#include "QtYaml.h"
#include "Settings.h"

QT_DEBUG_ADD_TYPE(IpTable::IpMapType)
QT_DEBUG_ADD_TYPE(IpTable::IpType)
QT_DEBUG_ADD_TYPE(IpTable::IpsType)

IpTable::IpTable() = default;

IpTable::~IpTable() = default;

bool IpTable::loadIp(IpType *ip, const QString &path)
{
    bool rtn = false;
    if (ip != nullptr)
    {
        QFile file(path);
        if (file.open(QIODevice::ReadOnly))
        {
            try
            {
                const std::string buffer = file.readAll().toStdString();
                const YAML::Node yaml_data = YAML::Load(buffer);
                YAML::convert<IpType>::decode(yaml_data, *ip);
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

bool IpTable::loadIp(IpType *ip, const QString &hal, const QString &name, const QString &ipName)
{
    bool rtn = false;
    if (ip != nullptr)
    {
        if (!hal.isEmpty() && !name.isEmpty() && !ipName.isEmpty())
        {
            const QString path = QString("%1/hal/%2/%3/ip/%4.yml")
                                     .arg(Settings.database(), hal.toLower(), name.toLower(), ipName.toLower());
            rtn = loadIp(ip, path);
        }
    }
    else
    {
        /** TODO: failed */
    }
    return rtn;
}

bool IpTable::loadIps(IpsType *ips, const QString &hal, const QString &name)
{
    bool rtn = false;
    if (ips != nullptr)
    {
        if (!hal.isEmpty() && !name.isEmpty())
        {
            const QString path = QString("%1/hal/%2/%3/ip").arg(Settings.database(), hal.toLower(), name.toLower());
            const QDir dir(path);
            QFileInfoList files = dir.entryInfoList({"*.yml"}, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
            if (!files.isEmpty())
            {
                for (const QFileInfo &file : files)
                {
                    IpType ip;
                    rtn = loadIp(&ip, file.absoluteFilePath());
                    if (!rtn)
                    {
                        break;
                    }
                    const QFileInfo info(file);
                    auto basename = info.baseName().toLower();
                    ips->insert(basename, ip);
                }
            }
            else
            {
                rtn = true;
            }

            static const QStringList list = {"gpio"};
            if (rtn)
            {
                for (const QString &file : list)
                {
                    IpType ip;
                    rtn = loadIp(&ip, QString(":/database/ip/%1.yml").arg(file));
                    if (!rtn)
                    {
                        break;
                    }
                    const QFileInfo info(file);
                    const QString basename = info.baseName().toLower();
                    if (ips->contains(basename))
                    {
                        IpType &ref_ip = (*ips)[basename];
                        auto ipIterator = ip.constBegin();
                        while (ipIterator != ip.constEnd())
                        {
                            ref_ip.insert(ipIterator.key(), ipIterator.value());
                            ++ipIterator;
                        }
                    }
                    else
                    {
                        ips->insert(basename, ip);
                    }
                }
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
