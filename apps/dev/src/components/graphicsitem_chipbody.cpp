/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        graphicsitem_chipbody.cpp
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
 *  2023-06-05     xqyjlj       initial version
 */

#include <QDebug>

#include "graphicsitem_chipbody.h"

static constexpr int margin = 6;

graphicsitem_chipbody::graphicsitem_chipbody(const qreal width, const qreal height, const QString &name,
                                             const QString &company, const QString &package)
{
    Q_ASSERT(width > 0 && height > 0);
    Q_ASSERT(!name.isEmpty());
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!package.isEmpty());

    _width = width;
    _height = height;
    _name = name.toUpper();
    _company = company;
    _package = package.toUpper();

    _font = new QFont("JetBrains Mono", QFont::ExtraBold);
    _font->setStyleStrategy(QFont::PreferAntialias);
}

graphicsitem_chipbody::~graphicsitem_chipbody()
{
    delete _font;
}

QRectF graphicsitem_chipbody::boundingRect() const
{
    return {0, 0, _width, _height};
}

QPainterPath graphicsitem_chipbody::shape() const
{
    QPainterPath path;
    path.addRect(boundingRect());
    return path;
}

void graphicsitem_chipbody::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    Q_UNUSED(widget)
    Q_UNUSED(option)

    const auto b = painter->brush();

    /******************** draw background **************************/
    painter->setRenderHint(QPainter::Antialiasing);
    painter->setBrush(QColor(50, 50, 50));
    painter->drawRect(0, 0, static_cast<int>(_width), static_cast<int>(_height));

    /******************** draw pin1 circle **************************/
    painter->setBrush(QColor(220, 230, 240));
    painter->drawEllipse(QRectF(margin * 2, margin * 2, 20.0, 20.0));

    /******************** draw text **************************/
    _font->setStyle(QFont::StyleNormal);
    _font->setPointSize(static_cast<int>(_width / 20));
    painter->setPen(QPen(QColor(255, 255, 255), 1));
    painter->setFont(*_font);
    const QFontMetrics fm(*_font);
    int pixels = fm.horizontalAdvance(_name);
    painter->drawText(QPointF((_width - pixels) / 2, _height / 2), _name);

    _font->setPointSize(static_cast<int>(_width / 30));
    _font->setStyle(QFont::StyleItalic);
    painter->setFont(*_font);

    pixels = static_cast<int>(fm.horizontalAdvance(_package) * 0.8);
    painter->drawText(QPointF((_width - pixels) / 2, _height * (0.9)), _package);

    const int height = fm.height();
    pixels = static_cast<int>(fm.horizontalAdvance(_company) * 0.8);
    painter->drawText(QPointF((_width - pixels) / 2, _height * (0.9) - height - 10), _company);

    /******************** draw border (with margin) **************************/
    QVarLengthArray<QLineF, 4> lines;
    lines.append(QLineF(margin, margin, margin, _height - margin));
    lines.append(QLineF(margin, margin, _width - margin, margin));
    lines.append(QLineF(_width - margin, _height - margin, margin, _height - margin));
    lines.append(QLineF(_width - margin, _height - margin, _width - margin, margin));
    painter->drawLines(lines.data(), lines.size());

    painter->setBrush(b);
}
