/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_os.cpp
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
 *  2023-06-03     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "os.h"

class testcase_os final : public QObject
{
    Q_OBJECT

  private slots:

    static void mkdir()
    {
        const auto string = "./test_mkdir";
        if (os::isdir(string))
            os::rmdir(string);

        os::mkdir(string);
        QVERIFY(!os::isdir(string));

        os::rmdir(string);
    }

    static void files()
    {
        auto list = os::files(".", "*.cmake");
        QVERIFY(!list.isEmpty());
        list = os::files(".", "*");
        QVERIFY(!list.isEmpty());
    }

    static void dirs()
    {
        auto list = os::dirs(".", "*_autogen");
        QVERIFY(!list.isEmpty());
        list = os::dirs(".", "*");
        QVERIFY(!list.isEmpty());
    }

    static void execv()
    {
        auto result = os::execv("git", QStringList() << "--version");
        QVERIFY(result);
        result = os::execv("not exits");
        QVERIFY(!result);
        result = os::execv("Makefile");
        QVERIFY(!result);

        QByteArray output, error;
        result = os::execv("git", QStringList() << "--version", {}, 30000, "", &output, &error);
        QVERIFY(result);
        QVERIFY(!output.isEmpty() && error.isEmpty());
        QVERIFY(output.startsWith("git version"));
    }

    static void readfile()
    {
        const auto result = os::readfile("./cmake_install.cmake");
        QVERIFY(!result.isEmpty());
    }

    static void writefile()
    {
        os::writefile("./.write_test", "test1");
        auto result = os::readfile("./.write_test");
        QVERIFY(!result.isEmpty());

        os::writefile("./.write_test", "test2", false);
        result = os::readfile("./.write_test");
        QVERIFY(result == "test1test2");
    }
};

QTEST_MAIN(testcase_os)

#include "testcase_os.moc"
