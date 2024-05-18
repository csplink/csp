/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        IpTable.h
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

#ifndef IP_TABLE_H
#define IP_TABLE_H

#include <QDebug>
#include <QMap>

class IpTable final
{
  public:
    typedef QMap<QString, QStringList> IpMapType;
    typedef QMap<QString, IpMapType> IpType;
    typedef QMap<QString, IpType> IpsType;

    static bool loadIp(IpType *ip, const QString &path);
    static bool loadIp(IpType *ip, const QString &hal, const QString &name, const QString &ipName);
    static bool loadIps(IpsType *ips, const QString &hal, const QString &name);

  private:
    explicit IpTable();
    ~IpTable();
};

QDebug operator<<(QDebug, const IpTable::IpMapType &);
QDebug operator<<(QDebug, const IpTable::IpType &);
QDebug operator<<(QDebug, const IpTable::IpsType &);

#endif /** IP_TABLE_H */
