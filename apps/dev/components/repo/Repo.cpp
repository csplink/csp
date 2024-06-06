/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        Repo.cpp
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

#include <QGlobalStatic>

#include "Repo.h"
#include "Settings.h"

Q_GLOBAL_STATIC(QScopedPointer<CspRepo>, instance)

CspRepo::CspRepo()
    : QObject(),
      m_repository(),
      m_isLoadedRepository(false),
      m_ips(),
      m_isLoadedIps(false),
      m_maps(),
      m_isLoadedMaps(false),
      m_chipSummary(),
      m_isLoadedChipSummary(false),
      m_hal(),
      m_vendor(),
      m_targetChip()
{
    RepositoryTable::loadRepository(&m_repository, Settings.database() + "/repository.yml");
}

CspRepo::~CspRepo() = default;

CspRepo &CspRepo::singleton()
{
    if (!*instance)
    {
        instance->reset(new CspRepo());
    }
    return **instance;
}

const RepositoryTable::RepositoryType &CspRepo::getRepository()
{
    if (!m_isLoadedRepository)
    {
        RepositoryTable::loadRepository(&m_repository, Settings.database() + "/repository.yml");
        m_isLoadedRepository = true;
    }
    return m_repository;
}

const MapTable::MapsType &CspRepo::getMaps(const QString &hal)
{
    if (hal != m_hal || !m_isLoadedMaps)
    {
        MapTable::loadMaps(&m_maps, hal);
        m_hal = hal;
        m_isLoadedMaps = true;
    }
    return m_maps;
}

const IpTable::IpsType &CspRepo::getIps(const QString &hal, const QString &targetChip)
{
    if (hal != m_hal || targetChip != m_targetChip || !m_isLoadedIps)
    {
        IpTable::loadIps(&m_ips, hal, targetChip);
        m_hal = hal;
        m_targetChip = targetChip;
        m_isLoadedIps = true;
    }
    return m_ips;
}

const ChipSummaryTable::ChipSummaryType &CspRepo::getChipSummary(const QString &vendor, const QString &targetChip)
{
    if (vendor != m_vendor || targetChip != m_targetChip || !m_isLoadedChipSummary)
    {
        ChipSummaryTable::loadChipSummary(&m_chipSummary, vendor, targetChip);
        m_vendor = vendor;
        m_targetChip = targetChip;
        m_isLoadedChipSummary = true;
    }
    return m_chipSummary;
}
