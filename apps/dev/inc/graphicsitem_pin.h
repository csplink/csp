/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        graphicsitem_pin.h
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

#ifndef CSP_GRAPHICSITEM_PIN_H
#define CSP_GRAPHICSITEM_PIN_H

#include <QFont>
#include <QFontMetrics>
#include <QGraphicsItem>
#include <QMenu>
#include <QPainter>
#include <QStyleOptionGraphicsItem>

#include "interface_graphicsitem_pin.h"
#include "pinout_table.h"
#include "project.h"

namespace csp {
class graphicsitem_pin : public QObject, public interface_graphicsitem_pin {
    Q_OBJECT
public:
    enum direction
    {
        TOP = 0,
        BOTTOM,
        LEFT,
        RIGHT
    };

public:
    explicit graphicsitem_pin(qreal width, qreal height);
    ~graphicsitem_pin() override;

    void    set_direction(enum direction direct);
    void    set_pinout_unit(pinout_table::pinout_unit_t *unit);
    void    set_selected(bool selected);
    void    set_name(const QString &name);
    QMenu  *get_menu() override;
    void    set_comment(const QString &comment);
    QString get_comment();

private slots:
    void menu_triggered_callback(QAction *action);

private:
    const QColor default_color  = QColor(185, 196, 202);
    const QColor power_color    = QColor(255, 246, 204);
    const QColor other_color    = QColor(187, 204, 0);
    const QColor selected_color = QColor(0, 204, 68);

    qreal                        _width;
    qreal                        _height;
    enum direction               _direction   = LEFT;
    pinout_table::pinout_unit_t *_pinout_unit = nullptr;
    bool                         _selected    = false;
    QString                      _name;
    QFont                       *_font;
    QFontMetrics                *_font_metrics;
    QString                      _comment;
    project                     *_project_instance;

    QMenu   *_menu                   = nullptr;
    QAction *_current_checked_action = nullptr;

protected:
    QRectF       boundingRect() const override;
    QPainterPath shape() const override;
    void         paint(QPainter *painter, const QStyleOptionGraphicsItem *option, QWidget *widget) override;
};
}  // namespace csp
#endif  // CSP_GRAPHICSITEM_PIN_H
