/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        Main.c
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License")
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2024-04-27     xqyjlj       initial version
 */

#include <QApplication>
#include <QtTest>

#include "TestCaseChipSummaryTable.h"
#include "TestCaseGit.h"
#include "TestCaseIpTable.h"
#include "TestCaseMapTable.h"
#include "TestCasePinoutTable.h"
#include "TestCaseProject.h"
#include "TestCaseProjectTable.h"
#include "TestCasePython.h"
#include "TestCaseQtJson.h"
#include "TestCaseRepositoryTable.h"
#include "TestCaseSettings.h"
#include "TestCaseToolCspRepo.h"
#include "TestCaseXMake.h"

#define TEST_EXEC(MODULE)                \
    do                                   \
    {                                    \
        MODULE test;                     \
        QTest::qExec(&test, argc, argv); \
    } while (0);

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);

    /** test components */
    {
        /** test components/git */
        {
            TEST_EXEC(TestCaseGit);
        }

        /** test components/parse */
        {
            TEST_EXEC(TestCaseQtJson);
        }

        /** test components/project */
        {
            TEST_EXEC(TestCaseProject);
            TEST_EXEC(TestCaseProjectTable);
        }

        /** test components/python */
        {
            TEST_EXEC(TestCasePython);
        }

        /** test components/repo */
        {
            TEST_EXEC(TestCaseChipSummaryTable);
            TEST_EXEC(TestCaseIpTable);
            TEST_EXEC(TestCaseMapTable);
            TEST_EXEC(TestCasePinoutTable);
            TEST_EXEC(TestCaseRepositoryTable);
        }

        /** test components/config */
        {
            TEST_EXEC(TestCaseSettings);
        }

        /** test components/tools */
        {
            TEST_EXEC(TestCaseToolCspRepo);
        }

        /** test components/xmake */
        {
            TEST_EXEC(TestCaseXMake);
        }
    }
}
