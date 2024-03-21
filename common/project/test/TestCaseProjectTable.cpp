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

#include "ProjectTable.h"

class TestCaseProjectTable final : public QObject
{
    Q_OBJECT

  private slots:

    static void loadProject()
    {
        ProjectTable::ProjectType project;
        ProjectTable::loadProject(&project, ":/project.json");
        QVERIFY(!project.Name.isEmpty());
    }

    static void saveProject()
    {
        auto p = ProjectTable::ProjectType();
        p.Name = "test";
        ProjectTable::PinConfigType pin_config;
        pin_config.Comment = "PA1-OUT";
        p.PinConfigs.insert("PA1", pin_config);
        ProjectTable::saveProject(p, "test.json");
        QVERIFY(QFile::exists("test.json"));
    }

    static void dumpProject()
    {
        auto p = ProjectTable::ProjectType();
        p.Name = "test";
        p.PinConfigs.insert("test", ProjectTable::PinConfigType());
        const auto str = ProjectTable::dumpProject(p);
        QVERIFY(!str.isEmpty());
    }
};

QTEST_MAIN(TestCaseProjectTable)

#include "TestCaseProjectTable.moc"
