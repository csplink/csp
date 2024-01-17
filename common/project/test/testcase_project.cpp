/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_project.cpp
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

#include <os.h>
#include <project.h>

project *g_project_instance = nullptr;

class testcase_project final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        project::init();
        g_project_instance = project::get_instance();
    }

    static void path()
    {
        g_project_instance->set_path("test");
        const auto path = g_project_instance->get_path();
        qDebug() << path;
        QVERIFY(path.endsWith("test"));
    }

    static void get_pin_config()
    {
        auto &cfg = g_project_instance->get_pin_config("PA1");
        cfg.comment = "PA1-OUT";

        QVERIFY(g_project_instance->get_pin_config("PA1").comment == "PA1-OUT");
    }

    static void cleanupTestCase()
    {
        project::deinit();
    }
};

QTEST_MAIN(testcase_project)

#include "testcase_project.moc"
