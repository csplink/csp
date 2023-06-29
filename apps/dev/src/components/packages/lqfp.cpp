/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        lqfp.cpp
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

#include <QDebug>

#include "lqfp.h"
#include "os.h"

#define LENGTH_OF_BODY (LQFP_PIN_SPACING + (LQFP_PIN_HEIGHT + LQFP_PIN_SPACING) * num)

lqfp::lqfp(QObject *parent) : QObject(parent) {}
lqfp::~lqfp() = default;

QList<QGraphicsItem *> lqfp::get_lqfp(const QString &hal, const QString &company, const QString &name)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    _pinout    = pinout_table::load_pinout(hal, name);
    _pin_count = _pinout.count();
    QList<QGraphicsItem *> items;
    QVector<QString>       vector(_pin_count);  // sort pinout

    auto num      = _pin_count / 4;
    auto pinout_i = _pinout.constBegin();
    while (pinout_i != _pinout.constEnd())
    {
        auto index    = pinout_i.value()->position - 1;
        vector[index] = pinout_i.key();
        pinout_i++;
    }

    int                         x;
    int                         y;
    int                         w;
    int                         h;
    graphicsitem_pin::direction direction;
    for (int i = 0; i < _pin_count; i++)
    {
        if (i < num)
        {
            auto index = i;
            direction  = graphicsitem_pin::direction::LEFT;
            w          = LQFP_PIN_WIDTH;
            h          = LQFP_PIN_HEIGHT;
            x          = 0;
            y          = index * (LQFP_PIN_HEIGHT + LQFP_PIN_SPACING) + LQFP_PIN_WIDTH + LQFP_PIN_SPACING;
        }
        else if (i >= num && i < 2 * num)
        {
            auto index = i - num;
            direction  = graphicsitem_pin::direction::BOTTOM;
            w          = LQFP_PIN_HEIGHT;
            h          = LQFP_PIN_WIDTH;
            x          = index * (LQFP_PIN_HEIGHT + LQFP_PIN_SPACING) + LQFP_PIN_WIDTH + LQFP_PIN_SPACING;
            y          = LQFP_PIN_WIDTH + LENGTH_OF_BODY;
        }
        else if (i >= 2 * num && i < 3 * num)
        {
            auto index = 3 * num - i;
            direction  = graphicsitem_pin::direction::RIGHT;
            w          = LQFP_PIN_WIDTH;
            h          = LQFP_PIN_HEIGHT;
            x          = LQFP_PIN_WIDTH + LENGTH_OF_BODY;
            y          = LQFP_PIN_WIDTH + LENGTH_OF_BODY - index * (LQFP_PIN_HEIGHT + LQFP_PIN_SPACING);
        }
        else
        {
            auto index = 4 * num - i;
            direction  = graphicsitem_pin::direction::TOP;
            w          = LQFP_PIN_HEIGHT;
            h          = LQFP_PIN_WIDTH;
            x          = LQFP_PIN_WIDTH + LENGTH_OF_BODY - index * (LQFP_PIN_HEIGHT + LQFP_PIN_SPACING);
            y          = 0;
        }
        auto *item = new graphicsitem_pin(w, h);
        item->set_name(vector.at(i));  // it must be called first
        item->set_direction(direction);
        item->set_pinout_unit(_pinout.value(vector.at(i)));
        item->setPos(QPointF(x, y));
        items << item;
    }

    auto *item =
        new graphicsitem_chipbody(LENGTH_OF_BODY, LENGTH_OF_BODY, name, company, "LQFP" + QString::number(_pin_count));
    item->setPos(QPointF(LQFP_PIN_WIDTH, LQFP_PIN_WIDTH));
    items << item;

    return items;
}
