/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        package_table.h
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
 *  2023-04-19     xqyjlj       initial version
 */

#ifndef CSP_PACKAGE_TABLE_H
#define CSP_PACKAGE_TABLE_H

#include "qtyaml.h"

class package_model {
public:
    struct
    {
        QString category;
        QString homepage;
        QString license;
        QString name;
        QString option;
        QString readme;
        QString rule;
        QString target;
    } package_model_t;

public:
};

#endif  // CSP_PACKAGE_TABLE_H
