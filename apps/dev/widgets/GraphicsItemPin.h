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

#ifndef __GRAPHICS_ITEM_PIN_H__
#define __GRAPHICS_ITEM_PIN_H__

#include "InterfaceGraphicsItemPin.h"
#include "PinoutTable.h"

class GraphicsItemPin final : public InterfaceGraphicsItemPin
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
    void setPinOutUnit(const PinoutTable::PinoutUnitType &unit);

    /**
     * @brief set pin name < it must be called first >
     * @param name: pin name
     */
    void setName(const QString &name);

  signals:
    void signalPropertyChanged(QGraphicsItem *item);

  private slots:
    void slotMenuTriggeredCallback(QAction *action);
    void slotProjectPinCommentChanged(const QString &name, const QString &oldValue, const QString &newValue);
    void slotProjectPinFunctionChanged(const QString &name, const QString &oldValue, const QString &newValue);
    void slotProjectPinLockedChanged(const QString &name, bool oldValue, bool newValue);

  private:
    static constexpr QColor defaultColor = QColor(185, 196, 202);
    static constexpr QColor powerColor = QColor(255, 246, 204);
    static constexpr QColor otherColor = QColor(187, 204, 0);
    static constexpr QColor selectedColor = QColor(0, 204, 68);

    qreal m_width;
    qreal m_height;
    int m_direction = LEFT;
    PinoutTable::PinoutUnitType m_pinoutUnit;
    bool m_locked = false;
    QString m_name;
    QFont *m_font;
    QFontMetrics *m_fontMetrics;
    QString m_comment;
    QString m_function;

    QMenu *m_menu = nullptr;
    QAction *m_previousCheckedAction = nullptr;
    QAction *m_currentCheckedAction = nullptr;

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

#endif /** __GRAPHICS_ITEM_PIN_H__ */
