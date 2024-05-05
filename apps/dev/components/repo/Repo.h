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

#ifndef __REPO_H__
#define __REPO_H__

#include <QFile>
#include <QObject>

#include "ChipSummaryTable.h"
#include "IpTable.h"
#include "MapTable.h"
#include "RepositoryTable.h"
#include "Settings.h"

class CspRepo final : public QObject
{
    Q_OBJECT

  public:
    CspRepo();
    ~CspRepo() override;

    static CspRepo &singleton();

    const RepositoryTable::RepositoryType &getRepository();
    const MapTable::MapsType &getMaps(const QString &hal);
    const IpTable::IpsType &getIps(const QString &hal, const QString &targetChip);
    const ChipSummaryTable::ChipSummaryType &getChipSummary(const QString &company, const QString &targetChip);

  private:
    RepositoryTable::RepositoryType m_repository;
    bool m_isLoadedRepository;
    IpTable::IpsType m_ips;
    bool m_isLoadedIps;
    MapTable::MapsType m_maps;
    bool m_isLoadedMaps;
    ChipSummaryTable::ChipSummaryType m_chipSummary;
    bool m_isLoadedChipSummary;
    QString m_hal;
    QString m_company;
    QString m_targetChip;

    Q_DISABLE_COPY_MOVE(CspRepo)
};

#define Repo CspRepo::singleton()

#endif /** __REPO_H__ */
