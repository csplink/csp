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
#include <QtTest>

#include "path.h"

class testcase_path : public QObject {
    Q_OBJECT

private slots:

    void basename()
    {
        // file
        auto basename_file = path::basename("./testcase_path.exe");
        QVERIFY(basename_file == "testcase_path");
        // dir
        auto basename_dir = path::basename(".");
        QVERIFY(basename_dir.isEmpty());
        // not exist
        auto basename_not_exist = path::basename("./not exist");
        QVERIFY(basename_not_exist.isEmpty());
    }

    void filename()
    {
        // file
        auto filename_file = path::filename("./testcase_path.exe");
        QVERIFY(filename_file == "testcase_path.exe");
        // dir
        auto filename_dir = path::filename(".");
        QVERIFY(filename_dir.isEmpty());
        // not exist
        auto filename_not_exist = path::filename("./not exist");
        QVERIFY(filename_not_exist.isEmpty());
    }

    void extension()
    {
        // file
        auto extension_file = path::extension("./testcase_path.exe");
        QVERIFY(extension_file == "exe");
        // dir
        auto extension_dir = path::extension(".");
        QVERIFY(extension_dir.isEmpty());
        // not exist
        auto extension_not_exist = path::extension("./not exist");
        QVERIFY(extension_not_exist.isEmpty());
    }

    void directory()
    {
        // file
        auto directory_file = path::directory("./testcase_path.exe");
        QVERIFY(!directory_file.isEmpty());
        // dir
        auto directory_dir = path::directory(".");
        QVERIFY(!directory_dir.isEmpty());
        // not exist
        auto directory_not_exist = path::directory("./not exist");
        QVERIFY(!directory_not_exist.isEmpty());
    }

    void relative()
    {
        // file
        auto relative_file = path::relative(path::appfile());
        QVERIFY(relative_file == "testcase_path.exe");
        relative_file = path::relative(path::appfile(), path::appdir() + "/..");
        QVERIFY(relative_file == "core/testcase_path.exe");
        // dir
        auto relative_dir = path::relative(path::appdir());
        QVERIFY(relative_dir == ".");
        relative_dir = path::relative(path::appdir(), path::appdir() + "/..");
        QVERIFY(relative_dir == "core");
        // not exist
        auto relative_not_exist = path::relative("./not exist");
        QVERIFY(relative_not_exist.isEmpty());
    }

    void absolute()
    {
        // file
        auto absolute_file = path::absolute("testcase_path.exe");
        QVERIFY(absolute_file == path::appfile());
        // dir
        auto absolute_dir = path::absolute(".");
        QVERIFY(absolute_dir == path::appdir() + "/.");
        // not exist
        auto absolute_not_exist = path::absolute("./not exist");
        QVERIFY(absolute_not_exist.isEmpty());
    }

    void is_absolute()
    {
        QVERIFY(path::is_absolute(path::appfile()));
        QVERIFY(!path::is_absolute("."));
    }
};

QTEST_MAIN(testcase_path)

#include "testcase_path.moc"
