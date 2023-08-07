/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        generate_code.h
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
 *  2023-07-03     xqyjlj       initial version
 */

#ifndef CSP_GENERATE_CODE_H
#define CSP_GENERATE_CODE_H

#include <QMap>

#include "project_table.h"

class generate_code {
public:
    typedef QMap<QString, QString> code_content_t;  // <file name, file content>

public:
    /**
     * @brief generate code file content from project table
     * @param project_table: project table
     * @return code file
     */
    static code_content_t generate_code_content(const project_table::project_t &project_table);

private:
    static QString generate_code_content_main(const project_table::project_t &project_table);

private:
    generate_code();
    ~generate_code();

    generate_code(const generate_code &signal);
    const generate_code &operator=(const generate_code &signal);
};

#endif  // CSP_GENERATE_CODE_H
