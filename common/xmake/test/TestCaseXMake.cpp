/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseXMake.cpp
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
 *  2023-08-14     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "Config.h"
#include "XMake.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCaseXMake final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Config::init();
        XMake::init();
    }

    static void version()
    {
        const auto result = XMake::version();
        qDebug().noquote() << QString("xmake version :%1").arg(result);
        QVERIFY(!result.isEmpty());
    }

    static void cleanupTestCase()
    {
        XMake::deinit();
        Config::deinit();
    }
};

QTEST_MAIN(TestCaseXMake)

#include "TestCaseXMake.moc"
