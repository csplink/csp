/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        LQFP.cpp
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

#include "GraphicsItemChipBody.h"
#include "LQFP.h"

static constexpr int LqfpPinWidth = 500;
static constexpr int LqfpPinHeight = 50;
static constexpr int LqfpPinSpacing = 6;

static constexpr int GetBodyLength(const int num)
{
    return LqfpPinSpacing + (LqfpPinHeight + LqfpPinSpacing) * num;
}

LQFP::LQFP(QObject *parent)
    : QObject(parent)
{
}

LQFP::~LQFP() = default;

QList<QGraphicsItem *> LQFP::getLqfp(const QString &hal, const QString &company, const QString &name)
{
    Q_ASSERT(!hal.isEmpty());
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!name.isEmpty());

    PinoutTable::loadPinout(&pinout_, company, hal, name);
    pinCount_ = pinout_.count();
    QList<QGraphicsItem *> items;
    QVector<QString> vector(pinCount_); // sort pinout

    const auto num = pinCount_ / 4;
    auto pinout_i = pinout_.constBegin();
    while (pinout_i != pinout_.constEnd())
    {
        const auto index = pinout_i.value().position - 1;
        vector[index] = pinout_i.key();
        ++pinout_i;
    }

    int x;
    int y;
    int w;
    int h;
    GraphicsItemPin::DirectionType direction;
    for (int i = 0; i < pinCount_; i++)
    {
        if (i < num)
        {
            const auto index = i;
            direction = GraphicsItemPin::DirectionType::LEFT;
            w = LqfpPinWidth;
            h = LqfpPinHeight;
            x = 0;
            y = index * (LqfpPinHeight + LqfpPinSpacing) + LqfpPinWidth + LqfpPinSpacing;
        }
        else if (i >= num && i < 2 * num)
        {
            const auto index = i - num;
            direction = GraphicsItemPin::DirectionType::BOTTOM;
            w = LqfpPinHeight;
            h = LqfpPinWidth;
            x = index * (LqfpPinHeight + LqfpPinSpacing) + LqfpPinWidth + LqfpPinSpacing;
            y = LqfpPinWidth + GetBodyLength(num);
        }
        else if (i >= 2 * num && i < 3 * num)
        {
            const auto index = 3 * num - i;
            direction = GraphicsItemPin::DirectionType::RIGHT;
            w = LqfpPinWidth;
            h = LqfpPinHeight;
            x = LqfpPinWidth + GetBodyLength(num);
            y = LqfpPinWidth + GetBodyLength(num) - index * (LqfpPinHeight + LqfpPinSpacing);
        }
        else
        {
            const auto index = 4 * num - i;
            direction = GraphicsItemPin::DirectionType::TOP;
            w = LqfpPinHeight;
            h = LqfpPinWidth;
            x = LqfpPinWidth + GetBodyLength(num) - index * (LqfpPinHeight + LqfpPinSpacing);
            y = 0;
        }
        auto *item = new GraphicsItemPin(w, h);
        item->setName(vector.at(i)); // it must be called first
        item->setDirection(direction);
        item->setPinOutUnit(pinout_[vector.at(i)]);
        item->setPos(QPointF(x, y));
        items << item;
    }

    auto *item = new GraphicsItemChipBody(GetBodyLength(num), GetBodyLength(num), name, company,
                                          "LQFP" + QString::number(pinCount_));
    item->setPos(QPointF(LqfpPinWidth, LqfpPinWidth));
    items << item;

    return items;
}
