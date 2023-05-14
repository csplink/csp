/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        csp_repo.h
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
 *  2023-05-11     xqyjlj       initial version
 */

#ifndef COMMON_REPO_CSP_REPO_H
#define COMMON_REPO_CSP_REPO_H

#include <QObject>

class csp_repo : public QObject {
    Q_OBJECT
public:
    static csp_repo *get_instance();

private:
    csp_repo();
    ~csp_repo() override;

    csp_repo(const csp_repo &signal);
    const csp_repo &operator=(const csp_repo &signal);

private:
    static csp_repo *_instance;
};

#endif  // COMMON_REPO_CSP_REPO_H