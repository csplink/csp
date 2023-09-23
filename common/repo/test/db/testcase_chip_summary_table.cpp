/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_chip_summary_table.cpp
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

#include <QtTest>

#include <chip_summary_table.h>

class testcase_chip_summary_table final : public QObject {
    Q_OBJECT

private slots:

    static void load_chip_summary()
    {
        const auto chip_summary = chip_summary_table::load_chip_summary(":/geehy/apm32f103zet6.yml");

        QVERIFY(!chip_summary.clocktree.isEmpty());
        QVERIFY(!chip_summary.company.isEmpty());
        QVERIFY(!chip_summary.hal.isEmpty());
        QVERIFY(!chip_summary.line.isEmpty());
        QVERIFY(!chip_summary.name.isEmpty());
        QVERIFY(!chip_summary.package.isEmpty());
        QVERIFY(!chip_summary.series.isEmpty());

        const auto company_url   = chip_summary.company_url;
        auto       company_url_i = company_url.constBegin();
        while (company_url_i != company_url.constEnd())
        {
            QVERIFY(!company_url_i.key().isEmpty());
            QVERIFY(!company_url_i.value().isEmpty());
            ++company_url_i;
        }

        const auto illustrate   = chip_summary.illustrate;
        auto       illustrate_i = illustrate.constBegin();
        while (illustrate_i != illustrate.constEnd())
        {
            QVERIFY(!illustrate_i.key().isEmpty());
            QVERIFY(!illustrate_i.value().isEmpty());
            ++illustrate_i;
        }

        const auto introduction   = chip_summary.introduction;
        auto       introduction_i = introduction.constBegin();
        while (introduction_i != introduction.constEnd())
        {
            QVERIFY(!introduction_i.key().isEmpty());
            QVERIFY(!introduction_i.value().isEmpty());
            ++introduction_i;
        }

        const auto url   = chip_summary.url;
        auto       url_i = url.constBegin();
        while (url_i != url.constEnd())
        {
            QVERIFY(!url_i.key().isEmpty());
            QVERIFY(!url_i.value().isEmpty());
            ++url_i;
        }

        const auto documents   = chip_summary.documents;
        auto       documents_i = documents.constBegin();
        while (documents_i != documents.constEnd())
        {
            QVERIFY(!documents_i.key().isEmpty());
            QVERIFY(!documents_i.value().isEmpty());

            auto document   = documents_i.value();
            auto document_i = document.constBegin();
            while (document_i != document.constEnd())
            {
                QVERIFY(!document_i.key().isEmpty());

                auto url1   = document_i.value().url;
                auto url1_i = url1.constBegin();
                while (url1_i != url.constEnd())
                {
                    QVERIFY(!url1_i.key().isEmpty());
                    QVERIFY(!url1_i.value().isEmpty());
                    ++url1_i;
                }
                ++document_i;
            }
            ++documents_i;
        }

        const auto modules   = chip_summary.modules;
        auto       modules_i = modules.constBegin();
        while (modules_i != modules.constEnd())
        {
            QVERIFY(!modules_i.key().isEmpty());
            QVERIFY(!modules_i.value().isEmpty());

            auto module   = modules_i.value();
            auto module_i = module.constBegin();
            while (module_i != module.constEnd())
            {
                QVERIFY(!module_i.key().isEmpty());

                auto description   = module_i.value().description;
                auto description_i = description.constBegin();
                while (description_i != description.constEnd())
                {
                    QVERIFY(!description_i.key().isEmpty());
                    QVERIFY(!description_i.value().isEmpty());
                    ++description_i;
                }
                ++module_i;
            }
            ++modules_i;
        }
    }
};

QTEST_MAIN(testcase_chip_summary_table)

#include "testcase_chip_summary_table.moc"