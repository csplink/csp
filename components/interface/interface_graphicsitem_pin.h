/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        interface_graphicsitem_pin.h
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
 *  2023-06-11     xqyjlj       initial version
 */

#ifndef CSP_INTERFACE_GRAPHICSITEM_PIN_H
#define CSP_INTERFACE_GRAPHICSITEM_PIN_H

#include <QGraphicsItem>
#include <QMenu>
#include <QPainter>
#include <QStyleOptionGraphicsItem>

#define GRAPHICSITEM_PIN_PROPERTY_NAME_MENU_PTR "user.menu.ptr"

namespace csp {
class interface_graphicsitem_pin : public QObject, public QGraphicsItem {
    Q_OBJECT
    Q_INTERFACES(QGraphicsItem)
};
}  // namespace csp

#endif  // CSP_INTERFACE_GRAPHICSITEM_PIN_H
