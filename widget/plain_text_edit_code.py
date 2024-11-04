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
# @file        plain_text_edit_view_code.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-27     xqyjlj       initial version
#

from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPaintEvent, QFont, QColor, QPainter
from PySide6.QtWidgets import QWidget
from qfluentwidgets import isDarkTheme, PlainTextEdit

from common import Style


class PlainTextEditCode(PlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabStopDistance(40)
        self.lineNumberArea = LineNumberArea(self)
        self.lineNumberAreaWidth = 0

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)

        self.updateLineNumberAreaWidth(0)

        Style.PLAIN_TEXT_EDIT_CODE.apply(self)

    def updateLineNumberAreaWidth(self, count: int):
        digits = 1
        maxDigs = max(1, count)
        while maxDigs >= 10:
            maxDigs //= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        rightMargin = self.lineNumberArea.RIGHT_MARGIN
        self.lineNumberAreaWidth = space + rightMargin

        self.setViewportMargins(self.lineNumberAreaWidth, 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth, cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.setPen(QColor("#8d96a0" if isDarkTheme() else "#929292"))
        painter.font().setBold(True)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber() + 1
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        areaWidth = self.lineNumberArea.width()
        rightMargin = self.lineNumberArea.RIGHT_MARGIN

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber)
                painter.drawText(0, int(top), areaWidth - rightMargin,
                                 self.fontMetrics().height(), Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


class LineNumberArea(QWidget):
    RIGHT_MARGIN = 10
    codeEditor = None

    def __init__(self, editor: PlainTextEditCode):
        super().__init__(editor)
        self.codeEditor = editor
        font = QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(9)
        font.setWeight(QFont.Weight.Light)
        self.setFont(font)

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth, 0)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        self.codeEditor.lineNumberAreaPaintEvent(event)
