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
        self.line_number_area = LineNumberArea(self)
        self.line_number_area_width = 0

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        self.update_line_number_area_width(0)

        Style.PLAIN_TEXT_EDIT_CODE.apply(self)

    def update_line_number_area_width(self, count: int):
        digits = 1
        max_digs = max(1, count)
        while max_digs >= 10:
            max_digs //= 10
            digits += 1

        space = 3 + self.fontMetrics().horizontalAdvance("9") * digits
        right_margin = self.line_number_area.RIGHT_MARGIN
        self.line_number_area_width = space + right_margin

        self.setViewportMargins(self.line_number_area_width, 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0, rect.y(), self.line_number_area.width(), rect.height()
            )

    # region overrides

    def resizeEvent(self, e):
        super().resizeEvent(e)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width, cr.height())
        )

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.line_number_area)
        painter.setPen(QColor("#8d96a0" if isDarkTheme() else "#929292"))
        painter.font().setBold(True)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber() + 1
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        area_width = self.line_number_area.width()
        right_margin = self.line_number_area.RIGHT_MARGIN

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number)
                painter.drawText(
                    0,
                    int(top),
                    area_width - right_margin,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    # endregion


class LineNumberArea(QWidget):
    RIGHT_MARGIN = 10
    code_editor = None

    def __init__(self, editor: PlainTextEditCode):
        super().__init__(editor)
        self.code_editor = editor
        font = QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(9)
        font.setWeight(QFont.Weight.Light)
        self.setFont(font)

    # region overrides

    def sizeHint(self) -> QSize:
        if self.code_editor is None:
            return QSize(0, 0)
        return QSize(self.code_editor.line_number_area_width, 0)

    def paintEvent(self, event: QPaintEvent):
        super().paintEvent(event)
        if self.code_editor is None:
            return
        self.code_editor.lineNumberAreaPaintEvent(event)

    # endregion
