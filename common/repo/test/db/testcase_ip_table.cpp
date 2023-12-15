/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_ip_table.cpp
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
 *  2023-06-17     xqyjlj       initial version
 */
#include <QDebug>
#include <QtTest>

#include "config.h"
#include <ip_table.h>

class testcase_ip_table final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Q_INIT_RESOURCE(repo);
        config::init();
    }

    static void load_ip()
    {
        ip_table::ip_t ip;
        ip_table::load_ip(&ip, ":/ip.yml");
        QVERIFY(!ip.isEmpty());
    }

    static void cleanupTestCase()
    {
        config::deinit();
        Q_CLEANUP_RESOURCE(repo);
    }
};

QTEST_MAIN(testcase_ip_table)

#include "testcase_ip_table.moc"
