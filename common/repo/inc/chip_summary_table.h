/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        chip_summary_table.h
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
 *  2023-05-21     xqyjlj       initial version
 */

#ifndef COMMON_REPO_CHIP_SUMMARY_TABLE_H
#define COMMON_REPO_CHIP_SUMMARY_TABLE_H

#include <QMap>

class chip_summary_table final
{
  public:
    typedef struct document_struct
    {
        QMap<QString, QString> url;
    } document_t;

    typedef struct module_struct
    {
        QMap<QString, QString> description;
    } module_t;

    typedef QMap<QString, QMap<QString, document_t>> documents_t;
    typedef QMap<QString, QMap<QString, module_t>> modules_t;

    typedef struct chip_summary_struct
    {
        QString clocktree;
        QString company;
        QMap<QString, QString> company_url;
        documents_t documents;
        QString hal;
        bool has_powerpad;
        QMap<QString, QString> illustrate;
        QMap<QString, QString> introduction;
        QString line;
        modules_t modules;
        QString name;
        QString package;
        QString series;
        QMap<QString, QString> url;
    } chip_summary_t;

  public:
    static chip_summary_t load_chip_summary(const QString &path);
    static chip_summary_t load_chip_summary(const QString &company, const QString &name);

  private:
    explicit chip_summary_table();
    ~chip_summary_table();
};

#endif // COMMON_REPO_CHIP_SUMMARY_TABLE_H
