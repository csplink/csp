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

#include <QFile>
#include <QObject>

#include "chip_summary_table.h"
#include "config.h"
#include "repository_table.h"

namespace csp {
class repo : public QObject {
    Q_OBJECT

public:
    const repository_table::repository_t *get_repository() const;

    inline chip_summary_table::chip_summary_t get_chip_summary(const QString &company, const QString &name)
    {
        return chip_summary_table::get_chip_summary(company, name);
    }

    inline bool chip_summary_exists(const QString &company, const QString &name)
    {
        return QFile::exists(
            QString("%1/db/chips/%2/%3.yml").arg(config::repodir(), company.toLower(), name.toLower()));
    }

private:
    repository_table::repository_t _repository;

public:
    static repo *get_instance();

private:
    repo();
    ~repo() override;

    repo(const repo &signal);
    const repo &operator=(const repo &signal);

private:
    static repo *_instance;
};
}  // namespace csp
#endif  // COMMON_REPO_CSP_REPO_H
