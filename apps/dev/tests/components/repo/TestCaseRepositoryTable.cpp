/**
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

#include "RepositoryTable.h"
#include "Settings.h"
#include "TestCaseRepositoryTable.h"

void TestCaseRepositoryTable::initTestCase()
{
}

void TestCaseRepositoryTable::loadRepository()
{
    RepositoryTable::RepositoryType repository;
    RepositoryTable::loadRepository(&repository, Settings.database() + "/repository.yml");
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

void TestCaseRepositoryTable::cleanupTestCase()
{
}
