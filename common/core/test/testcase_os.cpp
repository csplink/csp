/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        testcase_os.cpp
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
 *  2023-06-03     xqyjlj       initial version
 */

#include <QDebug>
#include <QtTest>

#include "os.h"

using namespace csp;

class testcase_os : public QObject {
    Q_OBJECT

private slots:

    void files()
    {
        auto list = os::files(".", "*.cmake");
        QVERIFY(!list.isEmpty());
        list = os::files(".", "*");
        QVERIFY(!list.isEmpty());
    }

    void dirs()
    {
        auto list = os::dirs(".", "*_autogen");
        QVERIFY(!list.isEmpty());
        list = os::dirs(".", "*");
        QVERIFY(!list.isEmpty());
    }
};

QTEST_MAIN(testcase_os)

#include "testcase_os.moc"
