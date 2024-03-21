/*
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        InterfaceGraphicsItemPin.h
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

#ifndef INTERFACE_GRAPHICS_ITEM_PIN_H
#define INTERFACE_GRAPHICS_ITEM_PIN_H

#include <QGraphicsItem>
#include <QMenu>
#include <QPainter>

class InterfaceGraphicsItemPin : public QObject, public QGraphicsItem
{
    Q_OBJECT
    Q_INTERFACES(QGraphicsItem)

  public:
    static constexpr const char *property_name_menu_ptr = "user.menu.ptr";
    static constexpr const char *property_name_pinout_unit_ptr = "user.pinout_unit.ptr";
};

#endif /** INTERFACE_GRAPHICS_ITEM_PIN_H */
