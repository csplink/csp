/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseIpTable.cpp
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

#include "Config.h"
#include "IpTable.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCaseIpTable final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Q_INIT_RESOURCE(repo);
        Config::init();
        Config::set("core/repoDir", QString(CSP_EXE_DIR) + "/repo");
    }

    static void loadIp()
    {
        IpTable::IpType ip;
        IpTable::loadIp(&ip, ":/lib/repo/db/ip/gpio.yml");
        QVERIFY(!ip.isEmpty());
    }

    static void cleanupTestCase()
    {
        Config::deinit();
        Q_CLEANUP_RESOURCE(repo);
    }
};

QTEST_MAIN(TestCaseIpTable)

#include "TestCaseIpTable.moc"
