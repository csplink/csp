/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseProjectTable.cpp
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
#include <ProjectTable.h>

class TestCaseProjectTable final : public QObject
{
    Q_OBJECT

  private slots:

    static void load_project()
    {
        ProjectTable::project_t project;
        ProjectTable::load_project(&project, ":/project.json");
        QVERIFY(!project.name.isEmpty());
    }

    static void save_project()
    {
        auto p = ProjectTable::project_t();
        p.name = "test";
        ProjectTable::pin_config_t pin_config;
        pin_config.comment = "PA1-OUT";
        p.pin_configs.insert("PA1", pin_config);
        ProjectTable::save_project(p, "test.json");
        QVERIFY(os::isfile("test.json"));
    }

    static void dump_project()
    {
        auto p = ProjectTable::project_t();
        p.name = "test";
        p.pin_configs.insert("test", ProjectTable::pin_config_t());
        const auto str = ProjectTable::dump_project(p);
        QVERIFY(!str.isEmpty());
    }
};

QTEST_MAIN(TestCaseProjectTable)

#include "TestCaseProjectTable.moc"
