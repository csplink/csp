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
# @file        base_highlighter.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-27     xqyjlj       initial version
#

from PySide6.QtGui import QSyntaxHighlighter, QFont, QColor, QTextCharFormat, QTextDocument


class BaseHighlighter(QSyntaxHighlighter):

    @staticmethod
    def format(color, style=''):
        char_format = QTextCharFormat()
        char_format.setForeground(color)
        if 'bold' in style:
            char_format.setFontWeight(QFont.Weight.Bold)
        if 'italic' in style:
            char_format.setFontItalic(True)

        return char_format

    STYLES = {
        'keyword': format(QColor("#c678dd"), 'bold'),
        'operator': format(QColor("#c678dd"), 'bold'),
        'brace': format(QColor("#d1a075")),
        'macro': format(QColor("#c678dd"), 'bold'),
        'string': format(QColor("#98c379")),
        'comment': format(QColor("#7f848e"), "italic"),
        'numbers': format(QColor("#d1a075")),
    }

    def __init__(self, document: QTextDocument):
        super().__init__(document)
