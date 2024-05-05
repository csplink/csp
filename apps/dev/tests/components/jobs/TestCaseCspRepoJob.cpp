/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        TestCaseCspRepoJob.cpp
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
 * 2024-04-29     xqyjlj       initial version
 */

#include <QtTest>

#include "CspRepoJob.h"
#include "TestCaseCspRepoJob.h"

void TestCaseCspRepoJob::initTestCase()
{
}

void TestCaseCspRepoJob::loadPackages()
{
    CspRepoJob::PackageType packages;

    CspRepoJob job("version");
    job.loadPackages(&packages);
    QVERIFY(!packages.isEmpty());

    packages.clear();
    job.loadPackages(&packages, "csp_hal_apm32f1");
    QVERIFY(!packages.isEmpty());
}

void TestCaseCspRepoJob::installPackage()
{
}
void TestCaseCspRepoJob::updatePackage()
{
}
void TestCaseCspRepoJob::uninstallPackage()
{
}

void TestCaseCspRepoJob::cleanupTestCase()
{
}
