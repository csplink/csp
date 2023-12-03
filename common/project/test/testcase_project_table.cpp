/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_project_table.cpp
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
 *  2023-05-28     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include <os.h>
#include <project_table.h>

class testcase_project_table final : public QObject
{
    Q_OBJECT

  private slots:

    static void load_project()
    {
        const auto p = project_table::load_project(":/project.json");
        QVERIFY(!p.core.name.isEmpty());
    }

    static void save_project()
    {
        auto p = project_table::project_t();
        p.core.name = "test";
        project_table::pin_config_t pin_config;
        pin_config.comment = "PA1-OUT";
        p.pin_configs.insert("PA1", pin_config);
        project_table::save_project(p, "test.json");
        QVERIFY(os::isfile("test.json"));
    }

    static void dump_project()
    {
        auto p = project_table::project_t();
        p.core.name = "test";
        p.pin_configs.insert("test", project_table::pin_config_t());
        const auto str = project_table::dump_project(p);
        QVERIFY(!str.isEmpty());
    }
};

QTEST_MAIN(testcase_project_table)

#include "testcase_project_table.moc"
