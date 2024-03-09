/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        LQFP.h
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
 *  2023-06-03     xqyjlj       initial version
 */

#ifndef LQFP_H
#define LQFP_H

#include "GraphicsItemPin.h"
#include "pinout_table.h"

class LQFP final : public QObject
{
    Q_OBJECT
  public:
    explicit LQFP(QObject *parent);
    ~LQFP() override;

    QList<QGraphicsItem *> getLqfp(const QString &hal, const QString &company, const QString &name);

  private:
    int pinCount_ = 0;
    pinout_table::pinout_t pinout_;
};

#endif // CSP_LQFP_H
