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
#include "os.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCaseChipSummaryTable final : public QObject
{
    Q_OBJECT

    static void check(const chip_summary_table::chip_summary_t &chip_summary)
    {
        QVERIFY(!chip_summary.clocktree.isEmpty());
        QVERIFY(!chip_summary.company.isEmpty());
        QVERIFY(!chip_summary.hal.isEmpty());
        QVERIFY(!chip_summary.line.isEmpty());
        QVERIFY(!chip_summary.name.isEmpty());
        QVERIFY(!chip_summary.package.isEmpty());
        QVERIFY(!chip_summary.series.isEmpty());
    }

  private slots:
    static void initTestCase()
    {
        Q_INIT_RESOURCE(repo);
        Config::init();
        Config::set("core/repoDir", QString(CSP_EXE_DIR) + "/repo");
    }

    static void load_chip_summary()
    {
        chip_summary_table::chip_summary_t chip_summary;
        for (const QString &dir : os::dirs(Config::repoDir() + "/db/chips", "*"))
        {
            for (const QString &file : os::files(dir, QString("*.yml")))
            {
                qDebug() << "Testing" << file;
                chip_summary_table::load_chip_summary(&chip_summary, file);
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
