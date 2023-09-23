/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_git.cpp
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

#include "git.h"

class testcase_git final : public QObject {
    Q_OBJECT

private slots:

    static void version()
    {
        const auto result = git::version();
        QVERIFY(!result.isEmpty());
    }

    static void variables()
    {
        auto result = git::variables(git::BRANCH);
        QVERIFY(!result.isEmpty());
        result = git::variables(git::COMMIT);
        QVERIFY(!result.isEmpty());
        result = git::variables(git::COMMIT_LONG);
        QVERIFY(!result.isEmpty());
        result = git::variables(git::COMMIT_DATE);
        QVERIFY(!result.isEmpty());
    }
};

QTEST_MAIN(testcase_git)

#include "testcase_git.moc"
