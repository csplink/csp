/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        logviewbox.cpp
 * @brief
 *
 *****************************************************************************
 * @attention
 * Licensed under the GNU General Public License v. 3 (the "License");
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.gnu.org/licenses/gpl-3.0.html
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * Copyright (C) 2023-2023 xqyjlj<xqyjlj@126.com>
 *
 *****************************************************************************
 * Change Logs:
 * Date           Author       Notes
 * ------------   ----------   -----------------------------------------------
 * 2023-12-24     xqyjlj       initial version
 */

#include <QPainter>
#include <QTextBlock>

#include "logviewbox.h"

logviewbox::logviewbox(QWidget *parent) : QPlainTextEdit(parent)
{
    _line_number_area = new line_number_area(this);

    connect(this, &logviewbox::blockCountChanged, this, &logviewbox::update_line_number_area_width,
            Qt::UniqueConnection);
    connect(this, &logviewbox::updateRequest, this, &logviewbox::update_line_number_area, Qt::UniqueConnection);

    update_line_number_area_width(0);

    // TODO: save to file
    const QFont font("JetBrains Mono");
    this->setFont(font);
}

logviewbox::~logviewbox() = default;

void logviewbox::line_number_area_paint_event(const QPaintEvent *event) const
{
    QPainter painter(_line_number_area);
    painter.fillRect(event->rect(), Qt::lightGray);

    QTextBlock block = firstVisibleBlock();
    int blockNumber = block.blockNumber();
    int top = qRound(blockBoundingGeometry(block).translated(contentOffset()).top());
    int bottom = top + qRound(blockBoundingRect(block).height());

    while (block.isValid() && top <= event->rect().bottom())
    {
        if (block.isVisible() && bottom >= event->rect().top())
        {
            QString number = QString::number(blockNumber + 1);
            painter.setPen(Qt::black);
            painter.drawText(0, top, _line_number_area->width(), fontMetrics().height(), Qt::AlignRight, number);
        }

        block = block.next();
        top = bottom;
        bottom = top + qRound(blockBoundingRect(block).height());
        ++blockNumber;
    }
}

int logviewbox::line_number_area_width() const
{
    int digits = 1;
    int max = qMax(1, blockCount());
    while (max >= 10)
    {
        max /= 10;
        ++digits;
    }

    const int space = 3 + fontMetrics().horizontalAdvance(QLatin1Char('9')) * digits;

    return space;
}

void logviewbox::append(const QString &text)
{
    this->appendPlainText(text); // TODO: add max
}

void logviewbox::resizeEvent(QResizeEvent *event)
{
    QPlainTextEdit::resizeEvent(event);

    const QRect cr = contentsRect();
    _line_number_area->setGeometry(QRect(cr.left(), cr.top(), line_number_area_width(), cr.height()));
}

void logviewbox::update_line_number_area_width(const int new_block_count)
{
    Q_UNUSED(new_block_count)

    setViewportMargins(line_number_area_width(), 0, 0, 0);
}

void logviewbox::update_line_number_area(const QRect &rect, int dy)
{
    if (dy)
    {
        _line_number_area->scroll(0, dy);
    }
    else
    {
        _line_number_area->update(0, rect.y(), _line_number_area->width(), rect.height());
    }

    if (rect.contains(viewport()->rect()))
    {
        update_line_number_area_width(0);
    }
}