/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        git.h
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
 *  2023-08-14     xqyjlj       initial version
 */

#ifndef CSP_COMMON_CORE_GIT_H
#define CSP_COMMON_CORE_GIT_H

#include "os.h"

class git final {
public:
    typedef enum
    {
        TAG = 0,      // "v0.0.0"
        TAG_LONG,     // "v0.0.0-0-2fc1f208"
        BRANCH,       // "generated-code-dev "
        COMMIT,       // "2fc1f208"
        COMMIT_LONG,  // "2fc1f208201480569aef0b19db1ec74b5d19ed1a"
        COMMIT_DATE   // "20230814164314"
    } variables_type;

public:
    /**
     * @brief get git version
     * @param program: program path or name
     * @return version; <example: "v2.34.1">
     */
    static QString version(const QString &program = "git");

    /**
     * @brief get git variables
     * @param type: type
     * @param program: program path or name
     * @param workdir: work dir
     * @return the variables corresponding to type
     */
    static QString variables(int type, const QString &program = "git", const QString &workdir = "");

private:
    git()  = default;
    ~git() = default;

    Q_DISABLE_COPY_MOVE(git)
};
#endif  //  CSP_COMMON_CORE_GIT_H
