/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCasePinoutTable.cpp
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
 *  2023-05-28     xqyjlj       initial version
 */
#include <QDebug>
#include <QFile>
#include <QtTest>

#include "Config.h"
#include "PinoutTable.h"

#ifndef CSP_EXE_DIR
#error please define CSP_EXE_DIR, which is csp.exe path
#endif

class TestCasePinoutTable final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase()
    {
        Q_INIT_RESOURCE(repo);
        Config::init();
        Config::set("core/repo", QString(CSP_EXE_DIR) + "/repo");
    }

    static void loadPinout()
    {
        PinoutTable::PinoutType pinout;
        const QDir dir1(Config::repoDir() + "/db/hal");
        const QFileInfoList companyDirs = dir1.entryInfoList({ "*" }, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
        for (const QFileInfo &companyDir : companyDirs)
        {
            const QDir dir2(companyDir.absoluteFilePath());
            const QFileInfoList halDirs = dir2.entryInfoList({ "*" }, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
            for (const QFileInfo &halDir : halDirs)
            {
                const QDir dir3(halDir.absoluteFilePath());
                const QFileInfoList chipDirs = dir3.entryInfoList({ "*" }, QDir::Dirs | QDir::NoDotAndDotDot | QDir::NoSymLinks);
                for (const QFileInfo &chipDir : chipDirs)
                {
                    const QString file = chipDir.absoluteFilePath() + "/pinout.yml";
                    QVERIFY(QFile::exists(file));

                    qDebug() << "Testing" << file;

                    PinoutTable::loadPinout(&pinout, file);
                    QVERIFY(!pinout.isEmpty());
                }
            }
        }
    }

    static void cleanupTestCase()
    {
        Config::deinit();
        Q_CLEANUP_RESOURCE(repo);
    }
};

QTEST_MAIN(TestCasePinoutTable)

#include "TestCasePinoutTable.moc"
