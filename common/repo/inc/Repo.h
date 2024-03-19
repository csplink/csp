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

#ifndef CSP_REPO_H
#define CSP_REPO_H

#include <QFile>
#include <QObject>

#include "Config.h"
#include "chip_summary_table.h"
#include "repository_table.h"

class repo final : public QObject
{
    Q_OBJECT

  public:
    /**
     * @brief init config
     */
    static void init();

    /**
     * @brief deinit config
     */
    static void deinit();

    const repository_table::repository_t *get_repository() const;

    static void load_chip_summary(chip_summary_table::chip_summary_t *chip_summary, const QString &company,
                                  const QString &name)
    {
        chip_summary_table::load_chip_summary(chip_summary, company, name);
    }

    static bool chip_summary_exists(const QString &company, const QString &name)
    {
        return QFile::exists(
            QString("%1/db/chips/%2/%3.yml").arg(Config::repodir(), company.toLower(), name.toLower()));
    }

    static repo *get_instance();

  private:
    inline static repo *_instance = nullptr;
    repository_table::repository_t _repository;

  private:
    repo();
    ~repo() override;

    Q_DISABLE_COPY_MOVE(repo)
};

#endif /** CSP_REPO_H */
