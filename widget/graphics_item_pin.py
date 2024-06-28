#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        graphics_item_pin.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-27     xqyjlj       initial version
#

from enum import Enum

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QFont, QPainterPath, QPainter, QColor, QPen, QFontMetrics
from PyQt5.QtWidgets import QGraphicsObject, QGraphicsItem, QWidget, QStyleOptionGraphicsItem, QAction
from qfluentwidgets import (isDarkTheme, CheckableMenu, Action)


class GraphicsItemPin(QGraphicsObject):
    pin_length = 100
    default_color = QColor(185, 196, 202)
    power_color = QColor(255, 246, 204)
    other_color = QColor(187, 204, 0)
    selected_color = QColor(0, 204, 68)

    m_locked = False
    m_comment = ""
    m_function = ""
    m_current_checked_action = None
    m_previous_checked_action = None

    class Direction(Enum):
        TOP = 1
        BOTTOM = 2
        LEFT = 3
        RIGHT = 4

    class Data(Enum):
        MENU = 1

    def __init__(self, width: int, height: int, direction: Direction, name: str, pinout_unit: dict):
        super().__init__()

        self.m_width = int(width)
        self.m_height = int(height)
        self.m_direction = direction
        self.m_name = name
        self.m_pinout_unit = pinout_unit

        self.m_font = QFont("JetBrains Mono", 14, QFont.Weight.Bold)
        self.m_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.m_font_metrics = QFontMetrics(self.m_font)

        self.m_menu = CheckableMenu()
        self.m_menu.view.setStyleSheet('''MenuActionListWidget {
                    font: 12px "JetBrains Mono", "Segoe UI", "Microsoft YaHei", "PingFang SC";
                    font-weight: normal;
            }''')
        self.m_menu.clear()
        self.m_menu.triggered.connect(self.menuTriggered)
        self.m_menu.addAction(Action(self.tr("Reset State")))
        self.m_menu.addSeparator()
        if "Functions" in pinout_unit:
            for name, function in pinout_unit["Functions"].items():
                action = Action(name)
                action.setCheckable(True)
                self.m_menu.addAction(action)

        self.setData(GraphicsItemPin.Data.MENU.value, self.m_menu)

        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.m_width, self.m_height)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        brush = painter.brush()

        # draw background
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        if self.m_pinout_unit["Type"] == "I/O":
            if (self.m_locked):
                painter.setBrush(self.selected_color)
            else:
                painter.setBrush(self.default_color)
        elif self.m_pinout_unit["Type"] == "Power":
            painter.setBrush(self.power_color)
        else:
            painter.setBrush(self.other_color)

        # draw body
        if (self.m_direction == GraphicsItemPin.Direction.LEFT):
            x = self.m_width - 100
            y = 0
            width = self.pin_length
            height = self.m_height
        elif (self.m_direction == GraphicsItemPin.Direction.BOTTOM):
            x = 0
            y = 0
            width = self.m_width
            height = self.pin_length
        elif (self.m_direction == GraphicsItemPin.Direction.RIGHT):
            x = 0
            y = 0
            width = self.pin_length
            height = self.m_height
        else:
            x = 0
            y = self.m_height - self.pin_length
            width = self.m_width
            height = self.pin_length

        painter.drawRect(x, y, width, height)

        # draw text
        if self.m_direction == GraphicsItemPin.Direction.LEFT or self.m_direction == GraphicsItemPin.Direction.RIGHT:
            text = self.m_font_metrics.elidedText(self.m_name, Qt.TextElideMode.ElideRight, self.pin_length - 20)
            painter.translate(10 + x, (self.m_height / 2) + 8)
        else:
            text = self.m_font_metrics.elidedText(self.m_name, Qt.TextElideMode.ElideRight, self.pin_length - 20)
            painter.translate((self.m_width / 2) + 8, self.pin_length - 10 + y)
            painter.rotate(-90)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setFont(self.m_font)
        painter.drawText(0, 0, text)

        # draw comment
        if self.m_comment == "":
            text = self.m_function
        else:
            text = f"{self.m_comment}({self.m_function})"

        if (self.m_direction == GraphicsItemPin.Direction.LEFT):
            text = self.m_font_metrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                  self.m_width - self.pin_length - 20)
            pixels = self.m_font_metrics.horizontalAdvance(text)
            painter.translate(-pixels - 20, 0)
        elif (self.m_direction == GraphicsItemPin.Direction.BOTTOM):
            text = self.m_font_metrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                  self.m_height - self.pin_length - 20)
            pixels = self.m_font_metrics.horizontalAdvance(text)
            painter.translate(-pixels - 20, 0)
        elif (self.m_direction == GraphicsItemPin.Direction.RIGHT):
            text = self.m_font_metrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                  self.m_width - self.pin_length - 20)
            painter.translate(self.pin_length, 0)
        else:
            text = self.m_font_metrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                  self.m_height - self.pin_length - 20)
            painter.translate(self.pin_length, 0)

        if isDarkTheme():
            painter.setPen(QPen(QColor(255, 255, 255), 1))

        painter.drawText(0, 0, text)
        painter.resetTransform()

        painter.setBrush(brush)

    def menuTriggered(self, action: QAction):
        self.m_current_checked_action = action
        if action.isCheckable():
            if self.m_previous_checked_action != None and self.m_previous_checked_action != action:
                self.m_previous_checked_action.setChecked(False)
            if action.isChecked():
                print(f"lock {action.text()}")
        else:
            if self.m_previous_checked_action != None:
                self.m_previous_checked_action.setChecked(False)
            self.m_previous_checked_action = None
            print(f"unlock {action.text()}")

        if self.m_previous_checked_action != action:
            self.m_previous_checked_action = action
