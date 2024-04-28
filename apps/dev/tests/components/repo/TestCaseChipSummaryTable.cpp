/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseChipSummaryTable.cpp
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

#include "Settings.h"
#include "TestCaseChipSummaryTable.h"

void TestCaseChipSummaryTable::check(const ChipSummaryTable::ChipSummaryType &chip_summary)
{
    QVERIFY(!chip_summary.ClockTree.isEmpty());
    QVERIFY(!chip_summary.Company.isEmpty());
    QVERIFY(!chip_summary.Hal.isEmpty());
    QVERIFY(!chip_summary.Line.isEmpty());
    QVERIFY(!chip_summary.Name.isEmpty());
    QVERIFY(!chip_summary.Package.isEmpty());
    QVERIFY(!chip_summary.Series.isEmpty());
}

void TestCaseChipSummaryTable::initTestCase()
{
}

void TestCaseChipSummaryTable::loadChipSummary()
{
    ChipSummaryTable::ChipSummaryType chip_summary;
    const QDir dir1(Settings.database() + "/chips");
    const QFileInfoList dirs = dir1.entryInfoList({ "*" }, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
    for (const QFileInfo &dir : dirs)
    {
        const QDir dir2(dir.absoluteFilePath());
        const QFileInfoList files = dir2.entryInfoList({ "*.yml" }, QDir::Files | QDir::Hidden | QDir::NoSymLinks);
        for (const QFileInfo &file : files)
        {
            qDebug() << "Testing" << file;
            ChipSummaryTable::loadChipSummary(&chip_summary, file.absoluteFilePath());
            check(chip_summary);
        }
    }
}

void TestCaseChipSummaryTable::cleanupTestCase()
{
}
