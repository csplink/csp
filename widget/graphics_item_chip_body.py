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
# @file        graphics_item_chip_body.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-24     xqyjlj       initial version
#

from PyQt5.QtCore import QRectF, QPointF, QLineF
from PyQt5.QtGui import QFont, QPainterPath, QPainter, QColor, QPen, QFontMetrics
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem


class GraphicsItemChipBody(QGraphicsItem):

    def __init__(self, width: int, height: int, name: str, vendor: str, package: str, parent=None):
        super().__init__(parent=parent)

        self.m_width = width
        self.m_height = height
        self.m_name = name.upper()
        self.m_vendor = vendor
        self.m_package = package.upper()
        self.m_margin = 6

        self.m_font = QFont("JetBrains Mono", QFont.Weight.ExtraBold)
        self.m_font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

    def boundingRect(self) -> QRectF:
        return QRectF(-0.5, -0.5, self.m_width + 1, self.m_height + 1)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        brush = painter.brush()

        # draw background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(50, 50, 50))
        painter.drawRect(0, 0, self.m_width, self.m_height)

        # draw pin1 circle
        painter.setBrush(QColor(220, 230, 240))
        painter.drawEllipse(QRectF(self.m_margin * 2, self.m_margin * 2, 20.0, 20.0))

        # draw text
        self.m_font.setStyle(QFont.Style.StyleNormal)
        self.m_font.setPointSize(int(self.m_width / 20))
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(self.m_font)
        fm = QFontMetrics(self.m_font)
        pixels = fm.horizontalAdvance(self.m_name)
        painter.drawText(QPointF((self.m_width - pixels) / 2, self.m_height / 2), self.m_name)

        self.m_font.setPointSize(int(self.m_width / 30))
        self.m_font.setStyle(QFont.Style.StyleItalic)
        painter.setFont(self.m_font)

        pixels = int(fm.horizontalAdvance(self.m_package) * 0.8)
        painter.drawText(QPointF((self.m_width - pixels) / 2, self.m_height * (0.9)), self.m_package)

        height = fm.height()
        pixels = int(fm.horizontalAdvance(self.m_vendor) * 0.8)
        painter.drawText(QPointF((self.m_width - pixels) / 2, self.m_height * (0.9) - height - 10), self.m_vendor)

        # draw border (with margin)
        painter.drawLine(QLineF(self.m_margin, self.m_margin, self.m_margin, self.m_height - self.m_margin))
        painter.drawLine(QLineF(self.m_margin, self.m_margin, self.m_width - self.m_margin, self.m_margin))
        painter.drawLine(
            QLineF(self.m_width - self.m_margin, self.m_height - self.m_margin, self.m_margin,
                   self.m_height - self.m_margin))
        painter.drawLine(
            QLineF(self.m_width - self.m_margin, self.m_height - self.m_margin, self.m_width - self.m_margin,
                   self.m_margin))

        painter.setBrush(brush)
