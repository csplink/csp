/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PinoutTable.h
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
 *  2023-05-28     xqyjlj       initial version
 */

#ifndef COMMON_REPO_CSP_PINOUT_TABLE_H
#define COMMON_REPO_CSP_PINOUT_TABLE_H

#include <QMap>

class pinout_table final
{
  public:
    typedef struct function_struct
    {
        QString mode;
        QString type;
    } function_t;

    typedef struct pinout_unit_struct
    {
        int position;
        QString type;
        QMap<QString, function_t> functions;
    } pinout_unit_t;

    typedef QMap<QString, pinout_unit_t> pinout_t;

  public:
    static void load_pinout(pinout_t *pinout, const QString &path);
    static void load_pinout(pinout_t *pinout, const QString &company, const QString &hal, const QString &name);

  private:
    explicit pinout_table();
    ~pinout_table();
};

Q_DECLARE_METATYPE(pinout_table::pinout_unit_t)
Q_DECLARE_METATYPE(pinout_table::pinout_unit_t *)

#endif // COMMON_REPO_CSP_PINOUT_TABLE_H
