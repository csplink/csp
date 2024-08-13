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
# @file        c_highlighter.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-27     xqyjlj       initial version
#

from PySide6.QtCore import Qt, QRegularExpression, QSize
from PySide6.QtGui import QSyntaxHighlighter, QTextDocument, QColor, QPainter, QTextFormat
from PySide6.QtWidgets import QTextEdit

from .base_highlighter import BaseHighlighter


class CHighlighter(BaseHighlighter):
    keywords = [
        "auto", "break", "case", "char", "const", "continue", "default", "do", "double", "else", "enum", "extern",
        "float", "for", "goto", "if", "inline", "int", "long", "register", "restrict", "return", "short", "signed",
        "sizeof", "static", "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
    ]

    operators = [
        '=', '==', '!=', '<', '<=', '>', '>=', '\+', '-', '\*', '/', '//', '\%', '\*\*', '\+=', '-=', '\*=', '/=',
        '\%=', '\^', '\|', '\&', '\~', '>>', '<<', "#"
    ]

    braces = ['\(', '\)', '\[', '\]']

    macros = ['#', "include", "ifndef", "define", "ifdef", "endif", "defined"]

    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self.multiline_comment = (QRegularExpression("/\*"), QRegularExpression("\*/"), 1, self.STYLES['comment'])

        rules = []

        rules += [(r'\b%s\b' % w, 0, self.STYLES['keyword']) for w in CHighlighter.keywords]
        rules += [(r'%s' % o, 0, self.STYLES['operator']) for o in CHighlighter.operators]
        rules += [(r'%s' % b, 0, self.STYLES['brace']) for b in CHighlighter.braces]
        rules += [(r'%s' % m, 0, self.STYLES['macro']) for m in CHighlighter.macros]

        rules += [
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.STYLES['string']),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.STYLES['string']),
            (r'\b[+-]?[0-9]+[lL]?\b', 0, self.STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.STYLES['numbers']),
            (r'//[^\n]*', 0, self.STYLES['comment']),
        ]

        self.rules = [(QRegularExpression(pat), index, fmt) for (pat, index, fmt) in rules]

    def highlightBlock(self, text: str):
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

        self.match_multiline(text, *self.multiline_comment)

    def match_multiline(self, text, delimiter_start, delimiter_end, in_state, style):
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        else:
            start = delimiter_start.indexIn(text)
            add = delimiter_start.matchedLength()

        while start >= 0:
            end = delimiter_end.indexIn(text, start + add)
            if end >= add:
                length = end - start + add + delimiter_end.matchedLength()
                self.setCurrentBlockState(0)
            else:
                self.setCurrentBlockState(in_state)
                length = len(text) - start + add

            self.setFormat(start, length, style)
            start = delimiter_start.indexIn(text, start + length)

        if self.currentBlockState() == in_state:
            return True
        else:
            return False
