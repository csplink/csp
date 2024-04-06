/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseRepositoryTable.cpp
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
 *  2023-05-03     xqyjlj       initial version
 */
#include <QDebug>
#include <QtTest>

#include "Config.h"
#include "RepositoryTable.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCaseRepositoryTable final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Q_INIT_RESOURCE(repo);
        Config::init();
        Config::set("core/repo", QString(CSP_EXE_DIR) + "/repo");
    }

    static void loadRepository()
    {
        RepositoryTable::RepositoryType repository;
        RepositoryTable::loadRepository(&repository, Config::repoDir() + "/db/repository.yml");
        const auto chips = repository.Chips;
        auto chips_i = chips.constBegin();
        while (chips_i != chips.constEnd())
        {
            QVERIFY(!chips_i.key().isEmpty());
            QVERIFY(!chips_i.value().isEmpty());

            auto company = chips_i.value();
            auto company_i = company.constBegin();
            while (company_i != company.constEnd())
            {
                QVERIFY(!company_i.key().isEmpty());
                QVERIFY(!company_i.value().isEmpty());

                auto series = company_i.value();
                auto series_i = series.constBegin();
                while (series_i != series.constEnd())
                {
                    QVERIFY(!series_i.key().isEmpty());
                    QVERIFY(!series_i.value().isEmpty());

                    auto line = series_i.value();
                    auto line_i = line.constBegin();
                    while (line_i != line.constEnd())
                    {
                        QVERIFY(!line_i.key().isEmpty());

                        auto mcu = line_i.value();
                        QVERIFY(!mcu.Core.isEmpty());
                        QVERIFY(!mcu.Package.isEmpty());

                        QVERIFY(!mcu.Peripherals.isEmpty());

                        QVERIFY(mcu.Flash > 0);
                        QVERIFY(mcu.Frequency > 0);
                        QVERIFY(mcu.IO > 0);
                        QVERIFY(mcu.Ram > 0);

                        QVERIFY(mcu.Current.Lowest > 0);
                        QVERIFY(mcu.Current.Run > 0);
                        QVERIFY(mcu.Temperature.Max > 0);
                        QVERIFY(mcu.Voltage.Max > 0);

                        ++line_i;
                    }
                    ++series_i;
                }
                ++company_i;
            }
            ++chips_i;
        }
    }

    static void cleanupTestCase()
    {
        Config::deinit();
        Q_CLEANUP_RESOURCE(repo);
    }
};

QTEST_MAIN(TestCaseRepositoryTable)

#include "TestCaseRepositoryTable.moc"
