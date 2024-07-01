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

from common import PROJECT


class GraphicsItemPin(QGraphicsObject):
    pin_length = 100
    default_color = QColor(185, 196, 202)
    power_color = QColor(255, 246, 204)
    other_color = QColor(187, 204, 0)
    selected_color = QColor(0, 204, 68)

    m_name = ""
    m_locked = False
    m_label = ""
    m_signal = ""
    m_current_checked_action = None
    m_previous_checked_action = None

    class Direction(Enum):
        TOP = 0
        BOTTOM = 1
        LEFT = 2
        RIGHT = 3

    class Data(Enum):
        MENU = 0
        LABEL = 1
        FUNCTION = 2
        LOCKED = 3

    def __init__(self, width: int, height: int, direction: Direction, name: str, pin_config: dict):
        super().__init__()

        self.m_width = int(width)
        self.m_height = int(height)
        self.m_direction = direction
        self.m_name = name
        self.m_pin_config = pin_config

        self.label_key = f"pin/{self.m_name}/label"
        self.signal_key = f"pin/{self.m_name}/signal"
        self.locked_key = f"pin/{self.m_name}/locked"

        self.setData(GraphicsItemPin.Data.LABEL.value, self.label_key)
        self.setData(GraphicsItemPin.Data.FUNCTION.value, self.signal_key)
        self.setData(GraphicsItemPin.Data.LOCKED.value, self.locked_key)

        self.m_label = PROJECT.config(self.label_key, "")
        self.m_signal = PROJECT.config(self.signal_key, "")
        self.m_locked = PROJECT.config(self.locked_key, False)

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
        if "signals" in pin_config:
            for name, signal in pin_config["signals"].items():
                action = Action(name)
                action.setCheckable(True)
                self.m_menu.addAction(action)

        self.setData(GraphicsItemPin.Data.MENU.value, self.m_menu)

        self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

        PROJECT.pinConfigChanged.connect(self.projectPinConfigChanged)

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
        if self.m_pin_config["type"] == "I/O":
            if (self.m_locked):
                painter.setBrush(self.selected_color)
            else:
                painter.setBrush(self.default_color)
        elif self.m_pin_config["type"] == "Power":
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

        # draw label
        if self.m_label == "":
            text = self.m_signal
        else:
            if self.m_signal == "":
                text = self.m_label
            else:
                text = f"{self.m_label}({self.m_signal})"

        if text != "":
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
                PROJECT.setConfig(self.locked_key, True)
                PROJECT.setConfig(self.signal_key, action.text())
        else:
            if self.m_previous_checked_action != None:
                self.m_previous_checked_action.setChecked(False)
            self.m_previous_checked_action = None
            PROJECT.setConfig(self.locked_key, False)
            PROJECT.setConfig(self.signal_key, "")

        if self.m_previous_checked_action != action:
            self.m_previous_checked_action = action

    def projectPinConfigChanged(self, key: str, value: str):
        if key[1] == self.m_name:
            if key[-1] == "label":
                self.m_label = value
            elif key[-1] == "locked":
                self.m_locked = value
            elif key[-1] == "signal":
                self.m_signal = value
            self.update()
