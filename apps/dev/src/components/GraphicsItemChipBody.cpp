/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        GraphicsItemChipBody.cpp
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

#include "GraphicsItemChipBody.h"

static constexpr int margin = 6;

GraphicsItemChipBody::GraphicsItemChipBody(const qreal width, const qreal height, const QString &name,
                                             const QString &company, const QString &package)
{
    Q_ASSERT(width > 0 && height > 0);
    Q_ASSERT(!name.isEmpty());
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!package.isEmpty());

    width_ = width;
    height_ = height;
    name_ = name.toUpper();
    company_ = company;
    package_ = package.toUpper();

    font_ = new QFont("JetBrains Mono", QFont::ExtraBold);
    font_->setStyleStrategy(QFont::PreferAntialias);
}

GraphicsItemChipBody::~GraphicsItemChipBody()
{
    delete font_;
}

QRectF GraphicsItemChipBody::boundingRect() const
{
    return {0, 0, width_, height_};
}

QPainterPath GraphicsItemChipBody::shape() const
{
    QPainterPath path;
    path.addRect(boundingRect());
    return path;
}

void GraphicsItemChipBody::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    Q_UNUSED(widget)
    Q_UNUSED(option)

    const auto b = painter->brush();

    /******************** draw background **************************/
    painter->setRenderHint(QPainter::Antialiasing);
    painter->setBrush(QColor(50, 50, 50));
    painter->drawRect(0, 0, static_cast<int>(width_), static_cast<int>(height_));

    /******************** draw pin1 circle **************************/
    painter->setBrush(QColor(220, 230, 240));
    painter->drawEllipse(QRectF(margin * 2, margin * 2, 20.0, 20.0));

    /******************** draw text **************************/
    font_->setStyle(QFont::StyleNormal);
    font_->setPointSize(static_cast<int>(width_ / 20));
    painter->setPen(QPen(QColor(255, 255, 255), 1));
    painter->setFont(*font_);
    const QFontMetrics fm(*font_);
    int pixels = fm.horizontalAdvance(name_);
    painter->drawText(QPointF((width_ - pixels) / 2, height_ / 2), name_);

    font_->setPointSize(static_cast<int>(width_ / 30));
    font_->setStyle(QFont::StyleItalic);
    painter->setFont(*font_);

    pixels = static_cast<int>(fm.horizontalAdvance(package_) * 0.8);
    painter->drawText(QPointF((width_ - pixels) / 2, height_ * (0.9)), package_);

    const int height = fm.height();
    pixels = static_cast<int>(fm.horizontalAdvance(company_) * 0.8);
    painter->drawText(QPointF((width_ - pixels) / 2, height_ * (0.9) - height - 10), company_);

    /******************** draw border (with margin) **************************/
    QVarLengthArray<QLineF, 4> lines;
    lines.append(QLineF(margin, margin, margin, height_ - margin));
    lines.append(QLineF(margin, margin, width_ - margin, margin));
    lines.append(QLineF(width_ - margin, height_ - margin, margin, height_ - margin));
    lines.append(QLineF(width_ - margin, height_ - margin, width_ - margin, margin));
    painter->drawLines(lines.data(), lines.size());

    painter->setBrush(b);
}
