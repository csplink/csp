/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        RepositoryTable.h
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the GNU Lesser General Public License v. 3 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.gnu.org/licenses/lgpl-3.0.html
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
 *  2023-04-20     xqyjlj       initial version
 */

#ifndef CSP_REPO_REPOSITORY_TABLE_H
#define CSP_REPO_REPOSITORY_TABLE_H

#include <QMap>

class RepositoryTable final
{
  public:
    typedef struct
    {
        float Lowest;
        float Run;
    } CurrentType;

    typedef struct
    {
        float Max;
        float Min;
    } TemperatureType;

    typedef struct
    {
        float Max;
        float Min;
    } VoltageType;

    typedef struct
    {
        QString Core;
        QString Company;
        QString Line;
        QString Series;
        QString Name;
        CurrentType Current;
        float Flash;
        float Frequency;
        int IO;
        QString Package;
        QMap<QString, int> Peripherals;
        float Price;
        float Ram;
        TemperatureType Temperature;
        VoltageType Voltage;
    } ChipInfoType;

    typedef QMap<QString, ChipInfoType> ChipLineType;

    typedef QMap<QString, ChipLineType> ChipSeriesType;

    typedef QMap<QString, ChipSeriesType> ChipCompanyType;

    typedef QMap<QString, ChipCompanyType> ChipType;

    typedef struct
    {
        ChipType Chips;
    } RepositoryType;

    static void loadRepository(RepositoryType *repository, const QString &path);

  private:
    explicit RepositoryTable();
    ~RepositoryTable();
};

#endif /** CSP_REPO_REPOSITORY_TABLE_H */
