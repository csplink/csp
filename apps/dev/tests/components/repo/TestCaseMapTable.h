/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TestCaseMapTable.h
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

#ifndef __TEST_CASE_MAP_TABLE_H__
#define __TEST_CASE_MAP_TABLE_H__

#include <QObject>

class TestCaseMapTable final : public QObject
{
    Q_OBJECT

  private slots:

    static void initTestCase();

    static void loadMap();

    static void cleanupTestCase();
};

#endif /** __TEST_CASE_MAP_TABLE_H__ */
