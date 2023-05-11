/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        common_repo.h
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

#ifndef CSP_COMMON_REPO_H
#define CSP_COMMON_REPO_H

#include <QObject>

class common_repo : public QObject {
    Q_OBJECT
public:
    static common_repo *get_instance();

private:
    common_repo();
    ~common_repo() override;

    common_repo(const common_repo &signal);
    const common_repo &operator=(const common_repo &signal);

private:
    static common_repo *_common_repo;
};

#endif  // CSP_COMMON_REPO_H
