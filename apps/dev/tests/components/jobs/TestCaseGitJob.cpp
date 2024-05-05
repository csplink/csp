/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        TestCaseGitJob.cpp
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

#include <QCoreApplication>
#include <QDebug>
#include <QtTest>

#include "GitJob.h"
#include "TestCaseGitJob.h"

void TestCaseGitJob::initTestCase()
{
}

void TestCaseGitJob::version()
{
    GitJob job("version", {});
    const auto result = job.version();
    qDebug().noquote() << QString("git version :%1").arg(result);
    QVERIFY(result != "not found");
}

void TestCaseGitJob::branch()
{
    GitJob job("branch", {});
    const auto result = job.branch(QCoreApplication::applicationDirPath());
    qDebug().noquote() << QString("git branch :%1").arg(result);
    QVERIFY(!result.contains(" "));
}

void TestCaseGitJob::commit()
{
    GitJob job("branch", {});
    const auto result = job.commit(QCoreApplication::applicationDirPath());
    qDebug().noquote() << QString("git commit :%1").arg(result);
    static QRegularExpression pattern("^[0-9a-fA-F]+$");
    QVERIFY(pattern.match(result).hasMatch());
    QVERIFY(result.length() == 7);
}

void TestCaseGitJob::commitLong()
{
    GitJob job("branch", {});
    const auto result = job.commitLong(QCoreApplication::applicationDirPath());
    qDebug().noquote() << QString("git commit long :%1").arg(result);
    static QRegularExpression pattern("^[0-9a-fA-F]+$");
    QVERIFY(pattern.match(result).hasMatch());
    QVERIFY(result.length() == 40);
}

void TestCaseGitJob::commitDate()
{
    GitJob job("branch", {});
    const auto result = job.commitDate(QCoreApplication::applicationDirPath());
    qDebug().noquote() << QString("git commit date :%1").arg(result);
    static QRegularExpression pattern("^\\d+$");
    QVERIFY(pattern.match(result).hasMatch());
}

void TestCaseGitJob::cleanupTestCase()
{
}
