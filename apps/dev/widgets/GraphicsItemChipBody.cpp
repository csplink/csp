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
    : QGraphicsItem(nullptr)
{
    Q_ASSERT(width > 0 && height > 0);
    Q_ASSERT(!name.isEmpty());
    Q_ASSERT(!company.isEmpty());
    Q_ASSERT(!package.isEmpty());

    m_width = width;
    m_height = height;
    m_name = name.toUpper();
    m_company = company;
    m_package = package.toUpper();

    m_font = new QFont("JetBrains Mono", QFont::ExtraBold);
    m_font->setStyleStrategy(QFont::PreferAntialias);
}

GraphicsItemChipBody::~GraphicsItemChipBody()
{
    delete m_font;
}

QRectF GraphicsItemChipBody::boundingRect() const
{
    return {0, 0, m_width, m_height};
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
    painter->drawRect(0, 0, static_cast<int>(m_width), static_cast<int>(m_height));

    /******************** draw pin1 circle **************************/
    painter->setBrush(QColor(220, 230, 240));
    painter->drawEllipse(QRectF(margin * 2, margin * 2, 20.0, 20.0));

    /******************** draw text **************************/
    m_font->setStyle(QFont::StyleNormal);
    m_font->setPointSize(static_cast<int>(m_width / 20));
    painter->setPen(QPen(QColor(255, 255, 255), 1));
    painter->setFont(*m_font);
    const QFontMetrics fm(*m_font);
    int pixels = fm.horizontalAdvance(m_name);
    painter->drawText(QPointF((m_width - pixels) / 2, m_height / 2), m_name);

    m_font->setPointSize(static_cast<int>(m_width / 30));
    m_font->setStyle(QFont::StyleItalic);
    painter->setFont(*m_font);

    pixels = static_cast<int>(fm.horizontalAdvance(m_package) * 0.8);
    painter->drawText(QPointF((m_width - pixels) / 2, m_height * (0.9)), m_package);

    const int height = fm.height();
    pixels = static_cast<int>(fm.horizontalAdvance(m_company) * 0.8);
    painter->drawText(QPointF((m_width - pixels) / 2, m_height * (0.9) - height - 10), m_company);

    /******************** draw border (with margin) **************************/
    QVarLengthArray<QLineF, 4> lines;
    lines.append(QLineF(margin, margin, margin, m_height - margin));
    lines.append(QLineF(margin, margin, m_width - margin, margin));
    lines.append(QLineF(m_width - margin, m_height - margin, margin, m_height - margin));
    lines.append(QLineF(m_width - margin, m_height - margin, m_width - margin, margin));
    painter->drawLines(lines.data(), lines.size());

    painter->setBrush(b);
}
