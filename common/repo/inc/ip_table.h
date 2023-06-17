/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ip_table.h
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

#ifndef CSP_IP_TABLE_H
#define CSP_IP_TABLE_H

#include "qtyaml.h"

namespace csp {
class ip_table {
public:
    typedef QMap<QString, QStringList> ip_map_t;
    typedef QMap<QString, ip_map_t>    ip_t;
    typedef QMap<QString, ip_t>        ips_t;

public:
    static ip_t  load_ip(const QString &path);
    static ip_t  load_ip(const QString &hal, const QString &name, const QString &ip);
    static ips_t load_ips(const QString &hal, const QString &name);

private:
    explicit ip_table();
    ~ip_table();
};
}  // namespace csp

#endif  // CSP_IP_TABLE_H
