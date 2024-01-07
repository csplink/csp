/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_xmake.cpp
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

#include "config.h"
#include "os.h"
#include "xmake.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class testcase_xmake final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        config::init();
        config::set("core/repodir", QString(CSP_EXE_DIR) + "/repo");
        config::set("core/xmake_repodir", QString(CSP_EXE_DIR) + "/xmake");
    }

    static void version()
    {
        const auto result = xmake::version();
        qDebug().noquote() << QString("xmake version :%1").arg(result);
        QVERIFY(!result.isEmpty());
    }

    static void lua()
    {
        const QByteArray data = os::readfile(":/test.lua");
        QVERIFY(!data.isEmpty());

        os::writefile("./test.lua", data);

        const auto result = xmake::lua("./test.lua");
#ifdef Q_OS_WINDOWS
        QVERIFY(result == "hello world\r\n");
#elif defined(Q_OS_LINUX)
        QVERIFY(result == "hello world\n");
#endif

        os::rm("./test.lua");
    }

    static void load_packages()
    {
        xmake::packages_t packages;
        xmake::load_packages(&packages);
        QVERIFY(!packages.toolchain.isEmpty());
        QVERIFY(!packages.library.isEmpty());
    }

    static void cleanupTestCase()
    {
        config::deinit();
    }
};

QTEST_MAIN(testcase_xmake)

#include "testcase_xmake.moc"
