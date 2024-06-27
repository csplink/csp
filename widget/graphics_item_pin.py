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

from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt
from PyQt5.QtGui import QFont, QPainterPath, QPainter, QColor, QPen, QFontMetrics
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem


class GraphicsItemPin(QGraphicsItem):
    pin_length = 100

    class Direction(Enum):
        TOP = 1
        BOTTOM = 2
        LEFT = 3
        RIGHT = 4

    def __init__(self, width: int, height: int, direction: Direction, name: str, parent=None):
        super().__init__(parent=parent)

        self.m_width = int(width)
        self.m_height = int(height)
        self.m_direction = direction
        self.m_name = name

        self.m_font = QFont("JetBrains Mono", QFont.Weight.ExtraBold)
        self.m_font.setPointSize(12)
        print(self.m_font.pointSize())
        self.m_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.m_font_metrics = QFontMetrics(self.m_font)

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
        painter.setBrush(brush)

        #  draw text
        if self.m_direction == GraphicsItemPin.Direction.LEFT or self.m_direction == GraphicsItemPin.Direction.RIGHT:
            text = self.m_font_metrics.elidedText(self.m_name, Qt.TextElideMode.ElideRight, self.pin_length - 20)
            painter.translate(10 + x, (self.m_height / 2) + 8)
        else:
            text = self.m_font_metrics.elidedText(self.m_name, Qt.TextElideMode.ElideRight, self.pin_length - 20)
            painter.translate((self.m_width / 2) + 8, self.pin_length - 10 + y)
            painter.rotate(-90)
        painter.setFont(self.m_font)
        painter.drawText(0, 0, text)
