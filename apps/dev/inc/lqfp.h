/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        lqfp.h
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

#ifndef CSP_LQFP_H
#define CSP_LQFP_H

#include "graphicsitem_pin.h"
#include "pinout_table.h"

#define LQFP_PIN_WIDTH   500
#define LQFP_PIN_HEIGHT  50
#define LQFP_PIN_SPACING 6

class lqfp final : public QObject
{
    Q_OBJECT
  public:
    explicit lqfp(QObject *parent);
    ~lqfp() override;

    QList<QGraphicsItem *> get_lqfp(const QString &hal, const QString &company, const QString &name);

  private:
    int _pin_count = 0;
    pinout_table::pinout_t _pinout;
};

#endif // CSP_LQFP_H
