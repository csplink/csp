/**
 *****************************************************************************
 * @author      xqyjlj
 * @file        LogBox.cpp
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

#include "LogBox.h"

LogBox::LogBox(QWidget *parent)
    : QPlainTextEdit(parent)
{
    lineNumberArea_ = new LineNumberArea(this);

    connect(this, &LogBox::blockCountChanged, this, &LogBox::updateLineNumberAreaWidth,
            Qt::UniqueConnection);
    connect(this, &LogBox::updateRequest, this, &LogBox::updateLineNumberArea, Qt::UniqueConnection);

    updateLineNumberAreaWidth(0);

    // TODO: save to file
    const QFont font("JetBrains Mono");
    this->setFont(font);
}

LogBox::~LogBox() = default;

void LogBox::lineNumberAreaPaintEvent(const QPaintEvent *event) const
{
    QPainter painter(lineNumberArea_);
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
            painter.drawText(0, top, lineNumberArea_->width(), fontMetrics().height(), Qt::AlignRight, number);
        }

        block = block.next();
        top = bottom;
        bottom = top + qRound(blockBoundingRect(block).height());
        ++blockNumber;
    }
}

int LogBox::lineNumberAreaWidth() const
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

void LogBox::append(const QString &text)
{
    this->appendPlainText(text); // TODO: add max
}

void LogBox::resizeEvent(QResizeEvent *event)
{
    QPlainTextEdit::resizeEvent(event);

    const QRect cr = contentsRect();
    lineNumberArea_->setGeometry(QRect(cr.left(), cr.top(), lineNumberAreaWidth(), cr.height()));
}

void LogBox::updateLineNumberAreaWidth(const int new_block_count)
{
    Q_UNUSED(new_block_count)

    setViewportMargins(lineNumberAreaWidth(), 0, 0, 0);
}

void LogBox::updateLineNumberArea(const QRect &rect, const int dy)
{
    if (dy)
    {
        lineNumberArea_->scroll(0, dy);
    }
    else
    {
        lineNumberArea_->update(0, rect.y(), lineNumberArea_->width(), rect.height());
    }

    if (rect.contains(viewport()->rect()))
    {
        updateLineNumberAreaWidth(0);
    }
}
