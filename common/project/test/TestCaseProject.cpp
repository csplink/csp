/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseProject.cpp
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
 *  2023-06-14     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "Project.h"

Project *ProjectInstance = nullptr;

class TestCaseProject final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Project::init();
        ProjectInstance = Project::getInstance();
    }

    static void path()
    {
        ProjectInstance->setPath("test");
        const auto path = ProjectInstance->getPath();
        qDebug() << path;
        QVERIFY(path.endsWith("test"));
    }

    static void getPinConfig()
    {
        auto &cfg = ProjectInstance->getPinConfig("PA1");
        cfg.comment = "PA1-OUT";

        QVERIFY(ProjectInstance->getPinConfig("PA1").comment == "PA1-OUT");
    }

    static void cleanupTestCase()
    {
        Project::deinit();
    }
};

QTEST_MAIN(TestCaseProject)

#include "TestCaseProject.moc"
