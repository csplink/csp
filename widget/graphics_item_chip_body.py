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

from PySide6.QtCore import QRectF, QPointF, QLineF
from PySide6.QtGui import QFont, QPainterPath, QPainter, QColor, QPen, QFontMetrics
from PySide6.QtWidgets import QGraphicsObject, QWidget, QStyleOptionGraphicsItem


class GraphicsItemChipBody(QGraphicsObject):

    def __init__(
        self, width: int, height: int, name: str, vendor: str, package: str, parent=None
    ):
        super().__init__(parent=parent)

        self.width = int(width)
        self.height = int(height)
        self.name = name.upper()
        self.vendor = vendor
        self.package = package.upper()
        self.margin = 6

        self.font = QFont("JetBrains Mono", QFont.Weight.ExtraBold)
        self.font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)

    # region overrides

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        brush = painter.brush()

        # draw background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(50, 50, 50))
        painter.drawRect(0, 0, self.width, self.height)

        # draw pin1 circle
        painter.setBrush(QColor(220, 230, 240))
        painter.drawEllipse(QRectF(self.margin * 2, self.margin * 2, 20.0, 20.0))

        # draw text
        self.font.setStyle(QFont.Style.StyleNormal)
        self.font.setPointSize(int(self.width / 20))
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        painter.setFont(self.font)
        fm = QFontMetrics(self.font)
        pixels = fm.horizontalAdvance(self.name)
        painter.drawText(QPointF((self.width - pixels) / 2, self.height / 2), self.name)

        self.font.setPointSize(int(self.width / 30))
        self.font.setStyle(QFont.Style.StyleItalic)
        painter.setFont(self.font)

        pixels = int(fm.horizontalAdvance(self.package) * 0.8)
        painter.drawText(
            QPointF((self.width - pixels) / 2, self.height * 0.9), self.package
        )

        height = fm.height()
        pixels = int(fm.horizontalAdvance(self.vendor) * 0.8)
        painter.drawText(
            QPointF((self.width - pixels) / 2, self.height * 0.9 - height - 10),
            self.vendor,
        )

        # draw border (with margin)
        painter.drawLine(
            QLineF(self.margin, self.margin, self.margin, self.height - self.margin)
        )
        painter.drawLine(
            QLineF(self.margin, self.margin, self.width - self.margin, self.margin)
        )
        painter.drawLine(
            QLineF(
                self.width - self.margin,
                self.height - self.margin,
                self.margin,
                self.height - self.margin,
            )
        )
        painter.drawLine(
            QLineF(
                self.width - self.margin,
                self.height - self.margin,
                self.width - self.margin,
                self.margin,
            )
        )

        painter.setBrush(brush)

    # endregion
