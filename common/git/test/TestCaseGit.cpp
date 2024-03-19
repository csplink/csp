/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseGit.cpp
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
 *  2023-08-14     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "Git.h"

class TestCaseGit final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        config::init();
    }

    static void version()
    {
        const auto result = Git::version();
        QVERIFY(!result.isEmpty());
    }

    static void variables()
    {
        auto result = Git::variables(Git::BRANCH);
        QVERIFY(!result.isEmpty());
        result = Git::variables(Git::COMMIT);
        QVERIFY(!result.isEmpty());
        result = Git::variables(Git::COMMIT_LONG);
        QVERIFY(!result.isEmpty());
        result = Git::variables(Git::COMMIT_DATE);
        QVERIFY(!result.isEmpty());
    }

    static void cleanupTestCase()
    {
        config::deinit();
    }
};

QTEST_MAIN(TestCaseGit)

#include "TestCaseGit.moc"
