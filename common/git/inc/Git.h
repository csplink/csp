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

#ifndef CSP_GIT_H
#define CSP_GIT_H

#include <QString>

#include "Config.h"

class Git final
{
  public:
    typedef enum
    {
        TAG = 0,     // "v0.0.0"
        TAG_LONG,    // "v0.0.0-0-2fc1f208"
        BRANCH,      // "generated-code-dev "
        COMMIT,      // "2fc1f208"
        COMMIT_LONG, // "2fc1f208201480569aef0b19db1ec74b5d19ed1a"
        COMMIT_DATE  // "20230814164314"
    } VariablesType;

    static bool execv(const QStringList &argv, QByteArray *output, QByteArray *error, const QString &workDir = Config::default_workdir());

    /**
     * @brief get git version
     * @return version; <example: "v2.34.1">
     */
    static QString version();

    /**
     * @brief get git variables
     * @param type: type
     * @param WorkDir: work dir
     * @return the variables corresponding to type
     */
    static QString variables(VariablesType type, const QString &WorkDir = "");

  private:
    Git() = default;
    ~Git() = default;

    Q_DISABLE_COPY_MOVE(Git)
};
#endif //  CSP_GIT_H
