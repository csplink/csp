/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        GraphicsItemPin.cpp
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
 *  2023-06-07     xqyjlj       initial version
 */

#include "GraphicsItemPin.h"
#include "Project.h"

GraphicsItemPin::GraphicsItemPin(const qreal width, const qreal height)
{
    Q_ASSERT(width > 0 && height > 0);
    Q_ASSERT(width > 100 || height > 100);

    m_width = width;
    m_height = height;

    m_font = new QFont("JetBrains Mono", 14, QFont::Bold);
    m_font->setStyleStrategy(QFont::PreferAntialias);
    m_fontMetrics = new QFontMetrics(*m_font);

    m_menu = new QMenu();
    m_menu->setFont(QFont("JetBrains Mono", 12));

    this->setFlags(ItemIsFocusable);
    this->setAcceptHoverEvents(true);
    this->setAcceptedMouseButtons(Qt::RightButton);

    (void)connect(m_menu, &QMenu::triggered, this, &GraphicsItemPin::slotMenuTriggeredCallback);
    (void)connect(&Project, &CspProject::signalPinCommentChanged, this, &GraphicsItemPin::slotProjectPinCommentChanged);
    (void)connect(&Project, &CspProject::signalPinFunctionChanged, this,
                  &GraphicsItemPin::slotProjectPinFunctionChanged);
    (void)connect(&Project, &CspProject::signalPinLockedChanged, this, &GraphicsItemPin::slotProjectPinLockedChanged);
}

GraphicsItemPin::~GraphicsItemPin()
{
    delete m_fontMetrics;
    delete m_font;
    delete m_menu;
    this->setProperty(property_name_pinout_unit_ptr, QVariant::fromValue(nullptr));
}

QRectF GraphicsItemPin::boundingRect() const
{
    return {0, 0, m_width, m_height};
}

QPainterPath GraphicsItemPin::shape() const
{
    QPainterPath path;
    path.addRect(boundingRect());
    return path;
}

void GraphicsItemPin::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    Q_UNUSED(widget)
    Q_UNUSED(option)
    // const qreal lod = option->levelOfDetailFromTransform(painter->worldTransform()); // get lod

    int x, y;
    int width, height;
    const auto b = painter->brush();
    /******************** draw background **************************/
    if (m_pinoutUnit.Type.toUpper() == "I/O")
    {
        if (m_locked)
        {
            painter->setBrush(selectedColor);
        }
        else
        {
            painter->setBrush(defaultColor);
        }
    }
    else if (m_pinoutUnit.Type.toUpper() == "POWER")
    {
        painter->setBrush(powerColor);
    }
    else
    {
        painter->setBrush(otherColor);
    }

    if (m_direction == LEFT)
    {
        x = static_cast<int>(m_width) - 100;
        y = 0;
        width = pinLength;
        height = static_cast<int>(m_height);
    }
    else if (m_direction == BOTTOM)
    {
        x = 0;
        y = 0;
        width = static_cast<int>(m_width);
        height = pinLength;
    }
    else if (m_direction == RIGHT)
    {
        x = 0;
        y = 0;
        width = pinLength;
        height = static_cast<int>(m_height);
    }
    else
    {
        x = 0;
        y = static_cast<int>(m_height) - pinLength;
        width = static_cast<int>(m_width);
        height = pinLength;
    }
    painter->drawRect(x, y, width, height);
    painter->setBrush(b);

    /******************** draw text **************************/
    QString text;
    if (m_direction == LEFT || m_direction == RIGHT)
    {
        text = m_fontMetrics->elidedText(m_name, Qt::ElideRight, pinLength - 20);
        painter->translate(10 + x, (m_height / 2) + 8);
    }
    else
    {
        text = m_fontMetrics->elidedText(m_name, Qt::ElideRight, pinLength - 20);
        painter->translate((m_width / 2) + 8, pinLength - 10 + y);
        painter->rotate(-90);
    }
    painter->setFont(*m_font);
    painter->drawText(0, 0, text);

    /******************** draw comment **************************/
    if (m_comment.isEmpty())
    {
        text = m_function;
    }
    else
    {
        text = QString("%1(%2)").arg(m_comment, m_function);
    }
    if (m_direction == LEFT)
    {
        text = m_fontMetrics->elidedText(text, Qt::ElideRight, static_cast<int>(m_width - pinLength - 20));
        const int pixels = m_fontMetrics->horizontalAdvance(text);
        painter->translate(-pixels - 20, 0);
    }
    else if (m_direction == BOTTOM)
    {
        text = m_fontMetrics->elidedText(text, Qt::ElideRight, static_cast<int>(m_height - pinLength - 20));
        const int pixels = m_fontMetrics->horizontalAdvance(text);
        painter->translate(-pixels - 20, 0);
    }
    else if (m_direction == RIGHT)
    {
        text = m_fontMetrics->elidedText(text, Qt::ElideRight, static_cast<int>(m_width - pinLength - 20));
        painter->translate(pinLength, 0);
    }
    else
    {
        text = m_fontMetrics->elidedText(text, Qt::ElideRight, static_cast<int>(m_height - pinLength - 20));
        painter->translate(pinLength, 0);
    }
    painter->drawText(0, 0, text);
    painter->resetTransform();
}

void GraphicsItemPin::setDirection(const int direct)
{
    m_direction = direct;
}

void GraphicsItemPin::setPinOutUnit(const PinoutTable::PinoutUnitType &unit)
{
    m_pinoutUnit = unit;
    m_menu->clear();
    m_menu->addAction(tr("Reset State"));
    m_menu->addSeparator();

    auto function_i = m_pinoutUnit.Functions.constBegin();
    while (function_i != m_pinoutUnit.Functions.constEnd())
    {
        auto *action = new QAction(m_menu);
        action->setText(function_i.key());
        action->setCheckable(true);
        m_menu->addAction(action);
        ++function_i;
    }
    this->setProperty(property_name_menu_ptr, QVariant::fromValue(m_menu));
    this->setProperty(property_name_pinout_unit_ptr, QVariant::fromValue(&m_pinoutUnit));

    m_comment = Project.pinComment(m_name);
    m_function = Project.pinFunction(m_name);
    m_locked = Project.pinLocked(m_name);
}

void GraphicsItemPin::setName(const QString &name)
{
    m_name = name;
    this->setToolTip(m_name);
    this->setObjectName(m_name);

    m_comment = Project.pinComment(m_name);
}

void GraphicsItemPin::slotMenuTriggeredCallback(QAction *action)
{
    m_currentCheckedAction = action;
    if (action->isCheckable())
    {
        if (m_previousCheckedAction != nullptr && m_previousCheckedAction != action)
        {
            m_previousCheckedAction->setChecked(false);
        }
        if (action->isChecked())
        {
            Project.setPinLocked(m_name, true);
            Project.setPinFunction(m_name, action->text());
        }
    }
    else // Reset State
    {
        if (m_previousCheckedAction != nullptr)
        {
            m_previousCheckedAction->setChecked(false);
        }
        m_previousCheckedAction = nullptr;
        Project.setPinLocked(m_name, false);
        Project.setPinFunction(m_name, "");
    }
    if (m_previousCheckedAction != action)
    {
        emit signalPropertyChanged(this);
        m_previousCheckedAction = action;
    }
}

void GraphicsItemPin::slotProjectPinCommentChanged(const QString &name, const QString &oldValue,
                                                   const QString &newValue)
{
    Q_UNUSED(oldValue)
    if (name == m_name)
    {
        m_comment = newValue;
        this->update();
    }
}

void GraphicsItemPin::slotProjectPinFunctionChanged(const QString &name, const QString &oldValue,
                                                    const QString &newValue)
{
    Q_UNUSED(oldValue)
    if (name == m_name)
    {
        m_function = newValue;
        this->update();
    }
}

void GraphicsItemPin::slotProjectPinLockedChanged(const QString &name, bool oldValue, bool newValue)
{
    Q_UNUSED(oldValue)
    if (name == m_name)
    {
        m_locked = newValue;
        this->update();
    }
}
