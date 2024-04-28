/**
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
 *  Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2024-04-27     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "Project.h"
#include "TestCaseProject.h"

static Project *ProjectInstance = nullptr;

void TestCaseProject::initTestCase()
{
    Project::init();
    ProjectInstance = Project::getInstance();
}

void TestCaseProject::path()
{
    ProjectInstance->setPath("test");
    const auto path = ProjectInstance->getPath();
    qDebug() << path;
    QVERIFY(path.endsWith("test"));
}

void TestCaseProject::getPinConfig()
{
    auto &cfg = ProjectInstance->getPinConfig("PA1");
    cfg.Comment = "PA1-OUT";

    QVERIFY(ProjectInstance->getPinConfig("PA1").Comment == "PA1-OUT");
}

void TestCaseProject::cleanupTestCase()
{
    Project::deinit();
}
