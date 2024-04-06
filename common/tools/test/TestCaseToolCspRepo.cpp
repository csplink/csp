/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        TestCaseToolCspRepo.cpp
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-04-06     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "Config.h"
#include "Python.h"
#include "ToolCspRepo.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCaseToolCspRepo final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Config::init();
        Python::init();
        Config::set("core/tools", QString(CSP_EXE_DIR) + "/tools");
    }

    static void loadPackages()
    {
        ToolCspRepo::PackageType packages;
        ToolCspRepo::loadPackages(&packages);
        qDebug().noquote() << packages;
        QVERIFY(!packages.isEmpty());

        packages.clear();
        ToolCspRepo::loadPackages(&packages, "csp_hal_apm32f1");
        qDebug().noquote() << packages;
        QVERIFY(!packages.isEmpty());
    }

    static void cleanupTestCase()
    {
        Python::deinit();
        Config::deinit();
    }
};

QTEST_MAIN(TestCaseToolCspRepo)

#include "TestCaseToolCspRepo.moc"
