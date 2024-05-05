/**
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
 *  Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2024-04-27     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "IpTable.h"
#include "TestCaseIpTable.h"

void TestCaseIpTable::initTestCase()
{
}

void TestCaseIpTable::loadIp()
{
    IpTable::IpType ip;
    bool rtn;
    rtn = IpTable::loadIp(&ip, ":/database/ip/gpio.yml");
    QVERIFY(rtn);
    QVERIFY(!ip.isEmpty());
}

void TestCaseIpTable::loadIps()
{
    IpTable::IpsType ips;
    bool rtn;
    rtn = IpTable::loadIps(&ips, "csp_hal_apm32f1", "apm32f103zet6");
    QVERIFY(rtn);
    QVERIFY(!ips.isEmpty());
}

void TestCaseIpTable::cleanupTestCase()
{
}
