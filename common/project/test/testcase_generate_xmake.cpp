/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_generate_xmake.cpp
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
 *  2023-11-19     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include <generate_xmake.h>
#include <os.h>
#include <project.h>

class testcase_generate_xmake final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Q_INIT_RESOURCE(project);
    }

    static void generate()
    {
        project_table::project_t p;
        project_table::load_project(&p, ":/project.json");
        QVERIFY(!p.core.name.isEmpty());

        const QString data = generate_xmake::generate(p);
        QVERIFY(!data.isEmpty());
        QVERIFY(!data.contains("${{"));

        os::writefile("./xmake.lua", data.toUtf8(), true);
    }

    static void cleanupTestCase()
    {
        Q_CLEANUP_RESOURCE(project);
    }
};

QTEST_MAIN(testcase_generate_xmake)

#include "testcase_generate_xmake.moc"
