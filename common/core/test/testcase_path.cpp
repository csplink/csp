/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_path.cpp
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
#include <QtGlobal>
#include <QtTest>

#include "path.h"

class testcase_path final : public QObject
{
    Q_OBJECT

  private slots:

    static void basename()
    {
        // file
        const auto basename_file = path::basename("./testcase_path.exe");
        QVERIFY(basename_file == "testcase_path");
        // dir
        const auto basename_dir = path::basename(".");
        QVERIFY(basename_dir.isEmpty());
        // not exist
        const auto basename_not_exist = path::basename("./not exist");
        QVERIFY(!basename_not_exist.isEmpty());
    }

    static void filename()
    {
        // file
        const auto filename_file = path::filename("./testcase_path.exe");
        QVERIFY(filename_file == "testcase_path.exe");
        // dir
        const auto filename_dir = path::filename(".");
        QVERIFY(filename_dir.isEmpty());
        // not exist
        const auto filename_not_exist = path::filename("./not exist");
        QVERIFY(!filename_not_exist.isEmpty());
    }

    static void extension()
    {
        // file
        const auto extension_file = path::extension("./testcase_path.exe");
        QVERIFY(extension_file == "exe");
        // dir
        const auto extension_dir = path::extension(".");
        QVERIFY(extension_dir.isEmpty());
        // not exist
        const auto extension_not_exist = path::extension("./not exist");
        QVERIFY(extension_not_exist.isEmpty());
    }

    static void directory()
    {
        // file
        const auto directory_file = path::directory("./testcase_path.exe");
        QVERIFY(!directory_file.isEmpty());
        // dir
        const auto directory_dir = path::directory(".");
        QVERIFY(!directory_dir.isEmpty());
        // not exist
        const auto directory_not_exist = path::directory("./not exist");
        QVERIFY(!directory_not_exist.isEmpty());
    }

    static void relative()
    {
        // file
        auto relative_file = path::relative(path::appfile());
#ifdef Q_OS_WINDOWS
        QVERIFY(relative_file == "testcase_path.exe");
#elif defined(Q_OS_LINUX)
        QVERIFY(relative_file == "testcase_path");
#endif
        relative_file = path::relative(path::appfile(), path::appdir() + "/..");
#ifdef Q_OS_WINDOWS
        QVERIFY(relative_file == "core/testcase_path.exe");
#elif defined(Q_OS_LINUX)
        QVERIFY(relative_file == "core/testcase_path");
#endif
        // dir
        auto relative_dir = path::relative(path::appdir());
        QVERIFY(relative_dir == ".");
        relative_dir = path::relative(path::appdir(), path::appdir() + "/..");
        QVERIFY(relative_dir == "core");
        // not exist
        const auto relative_not_exist = path::relative("./not exist");
        QVERIFY(relative_not_exist.isEmpty());
    }

    static void absolute()
    {
        // file

#ifdef Q_OS_WINDOWS
        auto absolute_file = path::absolute("testcase_path.exe");
#elif defined(Q_OS_LINUX)
        auto absolute_file = path::absolute("testcase_path");
#endif
        QVERIFY(absolute_file == path::appfile());
        // dir
        const auto absolute_dir = path::absolute(".");
        QVERIFY(absolute_dir == path::appdir() + "/.");
        // not exist
        const auto absolute_not_exist = path::absolute("./not exist");
        QVERIFY(absolute_not_exist.isEmpty());
    }

    static void is_absolute()
    {
        QVERIFY(path::is_absolute(path::appfile()));
        QVERIFY(!path::is_absolute("."));
    }
};

QTEST_MAIN(testcase_path)

#include "testcase_path.moc"
