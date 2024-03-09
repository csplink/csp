/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        GraphicsItemPin.h
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

#ifndef GRAPHICS_ITEM_PIN_H
#define GRAPHICS_ITEM_PIN_H

#include "interface_graphicsitem_pin.h"
#include "pinout_table.h"
#include "project.h"

class GraphicsItemPin final : public interface_graphicsitem_pin
{
    Q_OBJECT
  public:
    typedef enum
    {
        TOP = 0,
        BOTTOM,
        LEFT,
        RIGHT
    } DirectionType;

    static constexpr int pinLength = 100;

    explicit GraphicsItemPin(qreal width, qreal height);
    ~GraphicsItemPin() override;

    /**
     * @brief set pin direction
     * @param direct: pin direction
     */
    void setDirection(int direct);

    /**
     * @brief set pin out unit
     * @param unit: pin out unit
     */
    void setPinOutUnit(const pinout_table::pinout_unit_t &unit);

    /**
     * @brief set pin name < it must be called first >
     * @param name: pin name
     */
    void setName(const QString &name);

  signals:
    void signalPropertyChanged(QGraphicsItem *item);

  private slots:
    /**
     * @brief menu triggered callback
     * @param action: triggered action
     */
    void menuTriggeredCallback(QAction *action);

    /**
     * @brief pin property changed callback
     * @param property: property name
     * @param name: pin name
     * @param old_value: old value
     * @param new_value: new value
     */
    void pinPropertyChangedCallback(const QString &property, const QString &name, const QVariant &old_value,
                                    const QVariant &new_value);

  private:
    static constexpr QColor defaultColor = QColor(185, 196, 202);
    static constexpr QColor powerColor = QColor(255, 246, 204);
    static constexpr QColor otherColor = QColor(187, 204, 0);
    static constexpr QColor selectedColor = QColor(0, 204, 68);

    qreal width_;
    qreal height_;
    int direction_ = LEFT;
    pinout_table::pinout_unit_t pinoutUnit_;
    bool locked_ = false;
    QString name_;
    QFont *font_;
    QFontMetrics *fontMetrics_;
    QString comment_;
    QString function_;
    project *projectInstance_;

    QMenu *menu_ = nullptr;
    QAction *previousCheckedAction_ = nullptr;
    QAction *currentCheckedAction_ = nullptr;

  protected:
    /**
     * @brief defines the outer bounds of the item as a rectangle;
     * @return bounding rectangle
     */
    QRectF boundingRect() const override;

    /**
     * @brief the shape of this item as a QPainterPath in local coordinates
     * @return shape
     */
    QPainterPath shape() const override;

    /**
     * @brief paint the contents of an item in local coordinates
     * @param painter: painter
     * @param option: style option
     * @param widget: widget
     */
    void paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;
};

#endif /** GRAPHICS_ITEM_PIN_H */
