/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_repository_table.cpp
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

#include <QtTest>

#include <repository_table.h>

class testcase_repository_table : public QObject {
    Q_OBJECT

private slots:

    static void constructor()
    {
        repository_table repo(":/repository.yml");

        auto repository   = repo.get_repository();
        auto repository_i = repository.constBegin();
        while (repository_i != repository.constEnd())
        {
            QVERIFY(!repository_i.key().isEmpty());
            QVERIFY(!repository_i.value().isEmpty());

            auto company   = repository_i.value();
            auto company_i = company.constBegin();
            while (company_i != company.constEnd())
            {
                QVERIFY(!company_i.key().isEmpty());
                QVERIFY(!company_i.value().isEmpty());

                auto series   = company_i.value();
                auto series_i = series.constBegin();
                while (series_i != series.constEnd())
                {
                    QVERIFY(!series_i.key().isEmpty());
                    QVERIFY(!series_i.value().isEmpty());

                    auto line   = series_i.value();
                    auto line_i = line.constBegin();
                    while (line_i != line.constEnd())
                    {
                        QVERIFY(!line_i.key().isEmpty());

                        auto mcu = line_i.value();
                        QVERIFY(!mcu.core.isEmpty());
                        QVERIFY(!mcu.package.isEmpty());

                        QVERIFY(!mcu.peripherals.isEmpty());

                        QVERIFY(mcu.flash > 0);
                        QVERIFY(mcu.frequency > 0);
                        QVERIFY(mcu.io > 0);
                        QVERIFY(mcu.ram > 0);

                        QVERIFY(mcu.current.lowest > 0);
                        QVERIFY(mcu.current.run > 0);
                        QVERIFY(mcu.temperature.max > 0);
                        QVERIFY(mcu.voltage.max > 0);

                        line_i++;
                    }
                    series_i++;
                }
                company_i++;
            }
            repository_i++;
        }
    }
};

QTEST_MAIN(testcase_repository_table)

#include "testcase_repository_table.moc"