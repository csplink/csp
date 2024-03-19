/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Repo.h
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

#include "ChipSummaryTable.h"
#include "Config.h"
#include "RepositoryTable.h"

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

    const RepositoryTable::RepositoryType *getRepository() const;

    static void loadChipSummary(ChipSummaryTable::ChipSummaryType *chipSummary, const QString &company, const QString &name)
    {
        ChipSummaryTable::loadChipSummary(chipSummary, company, name);
    }

    static bool chipSummaryExists(const QString &company, const QString &name)
    {
        return QFile::exists(QString("%1/db/chips/%2/%3.yml").arg(Config::repoDir(), company.toLower(), name.toLower()));
    }

    static repo *getInstance();

  private:
    inline static repo *instance_ = nullptr;
    RepositoryTable::RepositoryType repository_;

    repo();
    ~repo() override;

    Q_DISABLE_COPY_MOVE(repo)
};

#endif /** CSP_REPO_H */
