/*
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
 *  Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2023-05-21     xqyjlj       initial version
 */
#include <QDebug>
#include <QtTest>

#include "ChipSummaryTable.h"
#include "Config.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCaseChipSummaryTable final : public QObject
{
    Q_OBJECT

    static void check(const ChipSummaryTable::ChipSummaryType &chip_summary)
    {
        QVERIFY(!chip_summary.ClockTree.isEmpty());
        QVERIFY(!chip_summary.Company.isEmpty());
        QVERIFY(!chip_summary.Hal.isEmpty());
        QVERIFY(!chip_summary.Line.isEmpty());
        QVERIFY(!chip_summary.Name.isEmpty());
        QVERIFY(!chip_summary.Package.isEmpty());
        QVERIFY(!chip_summary.Series.isEmpty());
    }

  private slots:
    static void initTestCase()
    {
        Q_INIT_RESOURCE(repo);
        Config::init();
        Config::set("core/repoDir", QString(CSP_EXE_DIR) + "/repo");
    }

    static void loadChipSummary()
    {
        ChipSummaryTable::ChipSummaryType chip_summary;
        const QDir dir1(Config::repoDir() + "/db/chips");
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

    static void cleanupTestCase()
    {
        Config::deinit();
        Q_CLEANUP_RESOURCE(repo);
    }
};

QTEST_MAIN(TestCaseChipSummaryTable)

#include "TestCaseChipSummaryTable.moc"
