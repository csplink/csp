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
    bool rtn;
    rtn = RepositoryTable::loadRepository(&repository, Settings.database() + "/repository.yml");
    QVERIFY(rtn);
    const RepositoryTable::ChipType &chips = repository.Chips;
    QMap<QString, RepositoryTable::ChipCompanyType>::const_iterator chipsI = chips.constBegin();
    while (chipsI != chips.constEnd())
    {
        QVERIFY(!chipsI.key().isEmpty());
        QVERIFY(!chipsI.value().isEmpty());

        const RepositoryTable::ChipCompanyType &company = chipsI.value();
        QMap<QString, RepositoryTable::ChipSeriesType>::const_iterator companyI = company.constBegin();
        while (companyI != company.constEnd())
        {
            QVERIFY(!companyI.key().isEmpty());
            QVERIFY(!companyI.value().isEmpty());

            const RepositoryTable::ChipSeriesType &series = companyI.value();
            QMap<QString, RepositoryTable::ChipLineType>::const_iterator seriesI = series.constBegin();
            while (seriesI != series.constEnd())
            {
                QVERIFY(!seriesI.key().isEmpty());
                QVERIFY(!seriesI.value().isEmpty());

                const RepositoryTable::ChipLineType &line = seriesI.value();
                QMap<QString, RepositoryTable::ChipInfoType>::const_iterator lineI = line.constBegin();
                while (lineI != line.constEnd())
                {
                    QVERIFY(!lineI.key().isEmpty());

                    const RepositoryTable::ChipInfoType &chip = lineI.value();
                    QVERIFY(!chip.Core.isEmpty());
                    QVERIFY(!chip.Package.isEmpty());

                    QVERIFY(!chip.Peripherals.isEmpty());

                    QVERIFY(chip.Flash > 0);
                    QVERIFY(chip.Frequency > 0);
                    QVERIFY(chip.IO > 0);
                    QVERIFY(chip.Ram > 0);

                    QVERIFY(chip.Current.Lowest > 0);
                    QVERIFY(chip.Current.Run > 0);
                    QVERIFY(chip.Temperature.Max > 0);
                    QVERIFY(chip.Voltage.Max > 0);

                    ++lineI;
                }
                ++seriesI;
            }
            ++companyI;
        }
        ++chipsI;
    }
}

void TestCaseRepositoryTable::cleanupTestCase()
{
}
