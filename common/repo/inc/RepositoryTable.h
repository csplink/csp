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

#ifndef COMMON_REPO_REPOSITORY_TABLE_H
#define COMMON_REPO_REPOSITORY_TABLE_H

#include <QMap>

class repository_table final
{
  public:
    typedef struct current_struct
    {
        float lowest;
        float run;
    } current_t;

    typedef struct temperature_struct
    {
        float max;
        float min;
    } temperature_t;

    typedef struct voltage_struct
    {
        float max;
        float min;
    } voltage_t;

    typedef struct chip_info_struct
    {
        QString core;
        QString company;
        QString line;
        QString series;
        QString name;
        current_t current;
        float flash;
        float frequency;
        int io;
        QString package;
        QMap<QString, int> peripherals;
        float price;
        float ram;
        temperature_t temperature;
        voltage_t voltage;
    } chip_info_t;

    typedef QMap<QString, chip_info_t> chip_line_t;

    typedef QMap<QString, chip_line_t> chip_series_t;

    typedef QMap<QString, chip_series_t> chip_company_t;

    typedef QMap<QString, chip_company_t> chip_t;

    typedef struct
    {
        chip_t chips;
    } repository_t;

  public:
    static void load_repository(repository_t *repository, const QString &path);

  private:
    explicit repository_table();
    ~repository_table();
};

#endif // COMMON_REPO_REPOSITORY_TABLE_H
