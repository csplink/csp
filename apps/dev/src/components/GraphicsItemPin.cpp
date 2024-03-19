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

#include <QDebug>

#include "GraphicsItemPin.h"

GraphicsItemPin::GraphicsItemPin(const qreal width, const qreal height)
{
    Q_ASSERT(width > 0 && height > 0);
    Q_ASSERT(width > 100 || height > 100);

    width_ = width;
    height_ = height;

    font_ = new QFont("JetBrains Mono", 14, QFont::Bold);
    font_->setStyleStrategy(QFont::PreferAntialias);
    fontMetrics_ = new QFontMetrics(*font_);

    menu_ = new QMenu();
    menu_->setFont(QFont("JetBrains Mono", 12));

    projectInstance_ = Project::getInstance();

    this->setFlags(ItemIsFocusable);
    this->setAcceptHoverEvents(true);
    this->setAcceptedMouseButtons(Qt::RightButton);

    connect(menu_, &QMenu::triggered, this, &GraphicsItemPin::menuTriggeredCallback, Qt::UniqueConnection);
    connect(projectInstance_, &Project::signalsPinPropertyChanged, this, &GraphicsItemPin::pinPropertyChangedCallback, Qt::UniqueConnection);
}

GraphicsItemPin::~GraphicsItemPin()
{
    delete fontMetrics_;
    delete font_;
    delete menu_;
    this->setProperty(property_name_pinout_unit_ptr, QVariant::fromValue(nullptr));
}

QRectF GraphicsItemPin::boundingRect() const
{
    return { 0, 0, width_, height_ };
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
    if (pinoutUnit_.type.toUpper() == "I/O")
    {
        if (locked_)
        {
            painter->setBrush(selectedColor);
        }
        else
        {
            painter->setBrush(defaultColor);
        }
    }
    else if (pinoutUnit_.type.toUpper() == "POWER")
    {
        painter->setBrush(powerColor);
    }
    else
    {
        painter->setBrush(otherColor);
    }

    if (direction_ == LEFT)
    {
        x = static_cast<int>(width_) - 100;
        y = 0;
        width = pinLength;
        height = static_cast<int>(height_);
    }
    else if (direction_ == BOTTOM)
    {
        x = 0;
        y = 0;
        width = static_cast<int>(width_);
        height = pinLength;
    }
    else if (direction_ == RIGHT)
    {
        x = 0;
        y = 0;
        width = pinLength;
        height = static_cast<int>(height_);
    }
    else
    {
        x = 0;
        y = static_cast<int>(height_) - pinLength;
        width = static_cast<int>(width_);
        height = pinLength;
    }
    painter->drawRect(x, y, width, height);
    painter->setBrush(b);

    /******************** draw text **************************/
    QString text;
    if (direction_ == LEFT || direction_ == RIGHT)
    {
        text = fontMetrics_->elidedText(name_, Qt::ElideRight, pinLength - 20);
        painter->translate(10 + x, (height_ / 2) + 8);
    }
    else
    {
        text = fontMetrics_->elidedText(name_, Qt::ElideRight, pinLength - 20);
        painter->translate((width_ / 2) + 8, pinLength - 10 + y);
        painter->rotate(-90);
    }
    painter->setFont(*font_);
    painter->drawText(0, 0, text);

    /******************** draw comment **************************/
    if (comment_.isEmpty())
    {
        text = function_;
    }
    else
    {
        text = QString("%1(%2)").arg(comment_, function_);
    }
    if (direction_ == LEFT)
    {
        text = fontMetrics_->elidedText(text, Qt::ElideRight, static_cast<int>(width_ - pinLength - 20));
        const int pixels = fontMetrics_->horizontalAdvance(text);
        painter->translate(-pixels - 20, 0);
    }
    else if (direction_ == BOTTOM)
    {
        text = fontMetrics_->elidedText(text, Qt::ElideRight, static_cast<int>(height_ - pinLength - 20));
        const int pixels = fontMetrics_->horizontalAdvance(text);
        painter->translate(-pixels - 20, 0);
    }
    else if (direction_ == RIGHT)
    {
        text = fontMetrics_->elidedText(text, Qt::ElideRight, static_cast<int>(width_ - pinLength - 20));
        painter->translate(pinLength, 0);
    }
    else
    {
        text = fontMetrics_->elidedText(text, Qt::ElideRight, static_cast<int>(height_ - pinLength - 20));
        painter->translate(pinLength, 0);
    }
    painter->drawText(0, 0, text);
    painter->resetTransform();
}

void GraphicsItemPin::setDirection(const int direct)
{
    direction_ = direct;
}

void GraphicsItemPin::setPinOutUnit(const PinoutTable::PinoutUnitType &unit)
{
    pinoutUnit_ = unit;
    menu_->clear();
    menu_->addAction(tr("Reset State"));
    menu_->addSeparator();

    auto function_i = pinoutUnit_.functions.constBegin();
    while (function_i != pinoutUnit_.functions.constEnd())
    {
        auto *action = new QAction(menu_);
        action->setText(function_i.key());
        action->setCheckable(true);
        menu_->addAction(action);
        ++function_i;
    }
    this->setProperty(property_name_menu_ptr, QVariant::fromValue(menu_));
    this->setProperty(property_name_pinout_unit_ptr, QVariant::fromValue(&pinoutUnit_));

    comment_ = projectInstance_->getPinComment(name_);
    function_ = projectInstance_->getPinFunction(name_);
    locked_ = projectInstance_->getPinLocked(name_);
}

void GraphicsItemPin::setName(const QString &name)
{
    name_ = name;
    this->setToolTip(name_);
    this->setObjectName(name_);

    comment_ = projectInstance_->getPinComment(name_);
}

void GraphicsItemPin::menuTriggeredCallback(QAction *action)
{
    currentCheckedAction_ = action;
    if (action->isCheckable())
    {
        if (previousCheckedAction_ != nullptr && previousCheckedAction_ != action)
        {
            previousCheckedAction_->setChecked(false);
        }
        if (action->isChecked())
        {
            projectInstance_->setPinLocked(name_, true);
            projectInstance_->setPinFunction(name_, action->text());
        }
    }
    else // Reset State
    {
        if (previousCheckedAction_ != nullptr)
        {
            previousCheckedAction_->setChecked(false);
        }
        previousCheckedAction_ = nullptr;
        projectInstance_->setPinLocked(name_, false);
        projectInstance_->setPinFunction(name_, "");
    }
    if (previousCheckedAction_ != action)
    {
        emit signalPropertyChanged(this);
        previousCheckedAction_ = action;
    }
}

void GraphicsItemPin::pinPropertyChangedCallback(const QString &property, const QString &name, const QVariant &old_value, const QVariant &new_value)
{
    Q_UNUSED(old_value)

    if (name != name_)
    {
        return;
    }

    if (property == "comment")
    {
        comment_ = new_value.toString();
    }
    else if (property == "function")
    {
        function_ = new_value.toString();
    }
    else if (property == "locked")
    {
        locked_ = new_value.toBool();
    }

    this->update();
}
