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

#include "graphicsitem_chipbody.h"
#include "lqfp.h"
#include "os.h"

static constexpr int lqfp_pin_width = 500;
static constexpr int lqfp_pin_height = 50;
static constexpr int lqfp_pin_spacing = 6;

static constexpr int get_body_length(const int num)
{
    return lqfp_pin_spacing + (lqfp_pin_height + lqfp_pin_spacing) * num;
}

lqfp::lqfp(QObject *parent) : QObject(parent)
{
}
lqfp::~lqfp() = default;

QList<QGraphicsItem *> lqfp::get_lqfp(const QString &hal, const QString &company, const QString &name)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    pinout_table::load_pinout(&_pinout, company, hal, name);
    _pin_count = _pinout.count();
    QList<QGraphicsItem *> items;
    QVector<QString> vector(_pin_count); // sort pinout

    const auto num = _pin_count / 4;
    auto pinout_i = _pinout.constBegin();
    while (pinout_i != _pinout.constEnd())
    {
        const auto index = pinout_i.value().position - 1;
        vector[index] = pinout_i.key();
        ++pinout_i;
    }

    int x;
    int y;
    int w;
    int h;
    graphicsitem_pin::direction direction;
    for (int i = 0; i < _pin_count; i++)
    {
        if (i < num)
        {
            const auto index = i;
            direction = graphicsitem_pin::direction::LEFT;
            w = lqfp_pin_width;
            h = lqfp_pin_height;
            x = 0;
            y = index * (lqfp_pin_height + lqfp_pin_spacing) + lqfp_pin_width + lqfp_pin_spacing;
        }
        else if (i >= num && i < 2 * num)
        {
            const auto index = i - num;
            direction = graphicsitem_pin::direction::BOTTOM;
            w = lqfp_pin_height;
            h = lqfp_pin_width;
            x = index * (lqfp_pin_height + lqfp_pin_spacing) + lqfp_pin_width + lqfp_pin_spacing;
            y = lqfp_pin_width + get_body_length(num);
        }
        else if (i >= 2 * num && i < 3 * num)
        {
            const auto index = 3 * num - i;
            direction = graphicsitem_pin::direction::RIGHT;
            w = lqfp_pin_width;
            h = lqfp_pin_height;
            x = lqfp_pin_width + get_body_length(num);
            y = lqfp_pin_width + get_body_length(num) - index * (lqfp_pin_height + lqfp_pin_spacing);
        }
        else
        {
            const auto index = 4 * num - i;
            direction = graphicsitem_pin::direction::TOP;
            w = lqfp_pin_height;
            h = lqfp_pin_width;
            x = lqfp_pin_width + get_body_length(num) - index * (lqfp_pin_height + lqfp_pin_spacing);
            y = 0;
        }
        auto *item = new graphicsitem_pin(w, h);
        item->set_name(vector.at(i)); // it must be called first
        item->set_direction(direction);
        item->set_pinout_unit(_pinout[vector.at(i)]);
        item->setPos(QPointF(x, y));
        items << item;
    }

    auto *item = new graphicsitem_chipbody(get_body_length(num), get_body_length(num), name, company,
                                           "LQFP" + QString::number(_pin_count));
    item->setPos(QPointF(lqfp_pin_width, lqfp_pin_width));
    items << item;

    return items;
}
