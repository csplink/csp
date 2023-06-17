/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        graphicsitem_pin.cpp
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

#include "graphicsitem_pin.h"

#define PIN_LENGTH 100

namespace csp {

graphicsitem_pin::graphicsitem_pin(qreal width, qreal height)
{
    Q_ASSERT(width > 0 && height > 0);
    Q_ASSERT(width > 100 || height > 100);

    _width  = width;
    _height = height;

    _font = new QFont("JetBrains Mono", 14, QFont::Bold);
    _font->setStyleStrategy(QFont::PreferAntialias);
    _font_metrics = new QFontMetrics(*_font);

    _menu = new QMenu();
    _menu->setFont(QFont("JetBrains Mono", 12));

    _project_instance = project::get_instance();

    this->setFlags(ItemIsPanel | ItemIsFocusable);
    this->setAcceptHoverEvents(true);
    this->setAcceptedMouseButtons(Qt::RightButton);

    connect(_menu, &QMenu::triggered, this, &graphicsitem_pin::menu_triggered_callback, Qt::UniqueConnection);
    connect(_project_instance, &project::pin_property_changed, this, &graphicsitem_pin::pin_property_changed_callback,
            Qt::UniqueConnection);
}

graphicsitem_pin::~graphicsitem_pin()
{
    delete _font_metrics;
    delete _font;
    delete _menu;
    delete _pinout_unit;
}

QRectF graphicsitem_pin::boundingRect() const
{
    return {0, 0, _width, _height};
}

QPainterPath graphicsitem_pin::shape() const
{
    QPainterPath path;
    path.addRect(boundingRect());
    return path;
}

void graphicsitem_pin::paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget)
{
    Q_UNUSED(widget);
    Q_UNUSED(option);
    // const qreal lod = option->levelOfDetailFromTransform(painter->worldTransform()); // get lod

    if (_pinout_unit == nullptr)
        return;

    int  x, y;
    int  width, height;
    auto b = painter->brush();
    /******************** draw background **************************/
    if (_pinout_unit->type.toUpper() == "I/O")
    {
        if (_selected)
            painter->setBrush(selected_color);
        else
            painter->setBrush(default_color);
    }
    else if (_pinout_unit->type.toUpper() == "POWER")
    {
        painter->setBrush(power_color);
    }
    else
    {
        painter->setBrush(other_color);
    }

    if (_direction == LEFT)
    {
        x      = (int)_width - 100;
        y      = 0;
        width  = PIN_LENGTH;
        height = (int)_height;
    }
    else if (_direction == BOTTOM)
    {
        x      = 0;
        y      = 0;
        width  = (int)_width;
        height = PIN_LENGTH;
    }
    else if (_direction == RIGHT)
    {
        x      = 0;
        y      = 0;
        width  = PIN_LENGTH;
        height = (int)_height;
    }
    else
    {
        x      = 0;
        y      = (int)_height - PIN_LENGTH;
        width  = (int)_width;
        height = PIN_LENGTH;
    }
    painter->drawRect(x, y, width, height);
    painter->setBrush(b);

    /******************** draw text **************************/
    QString text;
    if (_direction == LEFT || _direction == RIGHT)
    {
        text = _font_metrics->elidedText(_name, Qt::ElideRight, (int)(PIN_LENGTH - 20));
        painter->translate(10 + x, (_height / 2) + 8);
    }
    else
    {
        text = _font_metrics->elidedText(_name, Qt::ElideRight, (int)(PIN_LENGTH - 20));
        painter->translate((_width / 2) + 8, PIN_LENGTH - 10 + y);
        painter->rotate(-90);
    }
    painter->setFont(*_font);
    painter->drawText(0, 0, text);

    /******************** draw comment **************************/
    if (_direction == LEFT)
    {
        text       = _font_metrics->elidedText(_comment, Qt::ElideRight, (int)(_width - PIN_LENGTH - 20));
        int pixels = _font_metrics->horizontalAdvance(text);
        painter->translate(-pixels - 20, 0);
    }
    else if (_direction == BOTTOM)
    {
        text       = _font_metrics->elidedText(_comment, Qt::ElideRight, (int)(_height - PIN_LENGTH - 20));
        int pixels = _font_metrics->horizontalAdvance(text);
        painter->translate(-pixels - 20, 0);
    }
    else if (_direction == RIGHT)
    {
        text = _font_metrics->elidedText(_comment, Qt::ElideRight, (int)(_width - PIN_LENGTH - 20));
        painter->translate(PIN_LENGTH, 0);
    }
    else
    {
        text = _font_metrics->elidedText(_comment, Qt::ElideRight, (int)(_height - PIN_LENGTH - 20));
        painter->translate(PIN_LENGTH, 0);
    }
    painter->drawText(0, 0, text);
    painter->resetTransform();
}

void graphicsitem_pin::set_direction(graphicsitem_pin::direction direct)
{
    _direction = direct;
}

void graphicsitem_pin::set_pinout_unit(pinout_table::pinout_unit_t *unit)
{
    _pinout_unit = unit;
    _menu->clear();
    _menu->addAction(tr("Reset State"));
    _menu->addSeparator();

    auto function_i = _pinout_unit->functions.constBegin();
    while (function_i != _pinout_unit->functions.constEnd())
    {
        auto *action = new QAction(_menu);
        action->setText(function_i.key());
        action->setCheckable(true);
        _menu->addAction(action);
        function_i++;
    }
    _pinout_unit->position = 0;
}

void graphicsitem_pin::set_selected(bool selected)
{
    _selected = selected;
    this->update();
}

void graphicsitem_pin::set_name(const QString &name)
{
    _name = name;
    this->setToolTip(_name);

    _comment = _project_instance->get_pin_comment(_name);
}

QMenu *graphicsitem_pin::get_menu()
{
    return _menu;
}

void graphicsitem_pin::menu_triggered_callback(QAction *action)
{
    _current_checked_action = action;
    if (action->isCheckable())
    {
        if (_previous_checked_action != nullptr && _previous_checked_action != action)
        {
            _previous_checked_action->setChecked(false);
        }
        if (action->isChecked())
        {
            set_selected(true);
            set_comment(action->text());
        }
    }
    else  // Reset State
    {
        if (_previous_checked_action != nullptr)
            _previous_checked_action->setChecked(false);
        _previous_checked_action = nullptr;
        set_selected(false);
        set_comment("");
    }
    _previous_checked_action = action;
}

void graphicsitem_pin::set_comment(const QString &comment)
{
    _project_instance->set_pin_comment(_name, comment);
}

void graphicsitem_pin::pin_property_changed_callback(const QString  &property,
                                                     const QString  &name,
                                                     const QVariant &old_value,
                                                     const QVariant &new_value)
{
    Q_UNUSED(old_value);

    if (name != _name)
        return;

    if (property == "comment")
    {
        _comment = new_value.toString();
        this->update();
    }
}

}  // namespace csp