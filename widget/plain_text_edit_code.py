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
# @file        plain_text_edit_code_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-27     xqyjlj       initial version
#

from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPaintEvent, QFont, QColor, QPainter, QTextFormat
from PyQt5.QtWidgets import QWidget, QTextEdit

from qfluentwidgets import isDarkTheme, PlainTextEdit

from common import Style


class PlainTextEditCode(PlainTextEdit):
    m_lineNumberArea = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabStopWidth(40)
        self.m_lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.highlightCurrentLine()

        Style.PLAIN_TEXT_EDIT_CODE.apply(self)

    def lineNumberAreaWidth(self):
        digits = 1
        max_digs = max(1, self.blockCount())
        while max_digs >= 10:
            max_digs //= 10
            digits += 1

        space = 3 + self.fontMetrics().width('9') * digits
        right_margin = self.m_lineNumberArea.RIGHT_MARGIN

        return space + right_margin

    def updateLineNumberAreaWidth(self, newBlockCount):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.m_lineNumberArea.scroll(0, dy)
        else:
            self.m_lineNumberArea.update(0, rect.y(), self.m_lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.m_lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        if not self.isReadOnly():
            extraSelections = []

            selection = QTextEdit.ExtraSelection()
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

            self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.m_lineNumberArea)
        painter.setPen(QColor("#8d96a0" if isDarkTheme() else "#929292"))
        font = painter.font()
        font.setBold(True)
        painter.setFont(font)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber() + 1
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        areaWidth = self.m_lineNumberArea.width()
        rightMargin = self.m_lineNumberArea.RIGHT_MARGIN

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

    def __init__(self, editor):
        super(LineNumberArea, self).__init__(editor)
        self.codeEditor = editor
        font = QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(9)
        font.setWeight(QFont.Weight.Light)
        self.setFont(font)

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event: QPaintEvent):
        self.codeEditor.lineNumberAreaPaintEvent(event)
