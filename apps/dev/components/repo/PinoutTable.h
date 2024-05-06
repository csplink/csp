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

#ifndef __PINOUT_TABLE_H__
#define __PINOUT_TABLE_H__

#include <QDebug>
#include <QMap>

class PinoutTable final
{
  public:
    typedef struct
    {
        QString Mode;
        QString Type;
    } FunctionType;

    typedef struct
    {
        int Position;
        QString Type;
        QMap<QString, FunctionType> Functions;
    } PinoutUnitType;

    typedef QMap<QString, PinoutUnitType> PinoutType;

    static bool loadPinout(PinoutType *pinout, const QString &path);
    static bool loadPinout(PinoutType *pinout, const QString &company, const QString &hal, const QString &name);

  private:
    explicit PinoutTable();
    ~PinoutTable();
};

Q_DECLARE_METATYPE(PinoutTable::PinoutUnitType)
Q_DECLARE_METATYPE(PinoutTable::PinoutUnitType *)

QDebug operator<<(QDebug, const PinoutTable::FunctionType &);
QDebug operator<<(QDebug, const PinoutTable::PinoutUnitType &);

#endif /** __PINOUT_TABLE_H__ */
