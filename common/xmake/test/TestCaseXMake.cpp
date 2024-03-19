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
        Config::set("core/xmakeRepoDir", QString(CSP_EXE_DIR) + "/xmake");
    }

    static void version()
    {
        const auto result = XMake::version();
        qDebug().noquote() << QString("xmake version :%1").arg(result);
        QVERIFY(!result.isEmpty());
    }

    static void lua()
    {
        QByteArray data;
        QFile resFile(":/test.lua");
        if (resFile.open(QIODevice::ReadOnly))
        {
            data = resFile.readAll();
            resFile.close();
        }
        QVERIFY(!data.isEmpty());

        QFile luaFile("./test.lua");
        if (luaFile.open(QIODevice::WriteOnly))
        {
            luaFile.write(data);
            luaFile.close();
        }

        const auto result = XMake::lua("./test.lua");
#ifdef Q_OS_WINDOWS
        QVERIFY(result == "hello world\r\n");
#elif defined(Q_OS_LINUX)
        QVERIFY(result == "hello world\n");
#endif

        QFile::remove("./test.lua");
    }

    static void load_packages()
    {
        XMake::PackageType packages;
        XMake::loadPackages(&packages);
        QVERIFY(!packages.isEmpty());
    }

    static void cleanupTestCase()
    {
        Config::deinit();
    }
};

QTEST_MAIN(TestCaseXMake)

#include "TestCaseXMake.moc"
