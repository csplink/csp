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

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QTextDocument

from .base_highlighter import BaseHighlighter


class CHighlighter(BaseHighlighter):
    keywords = [
        "auto",
        "break",
        "case",
        "char",
        "const",
        "continue",
        "default",
        "do",
        "double",
        "else",
        "enum",
        "extern",
        "float",
        "for",
        "goto",
        "if",
        "inline",
        "int",
        "long",
        "register",
        "restrict",
        "return",
        "short",
        "signed",
        "sizeof",
        "static",
        "struct",
        "switch",
        "typedef",
        "union",
        "unsigned",
        "void",
        "volatile",
        "while",
    ]

    operators = [
        "=",
        "==",
        "!=",
        "<",
        "<=",
        ">",
        ">=",
        "\+",
        "-",
        "\*",
        "/",
        "//",
        "\%",
        "\*\*",
        "\+=",
        "-=",
        "\*=",
        "/=",
        "\%=",
        "\^",
        "\|",
        "\&",
        "\~",
        ">>",
        "<<",
        "#",
    ]

    braces = ["\(", "\)", "\[", "\]"]

    macros = ["#", "include", "ifndef", "define", "ifdef", "endif", "defined"]

    def __init__(self, document: QTextDocument):
        super().__init__(document)

        self.multiline_comment = (
            QRegularExpression("/\*"),
            QRegularExpression("\*/"),
            1,
            self.STYLES["comment"],
        )

        rules = []

        rules += [
            (r"\b%s\b" % w, 0, self.STYLES["keyword"]) for w in CHighlighter.keywords
        ]
        rules += [
            (r"%s" % o, 0, self.STYLES["operator"]) for o in CHighlighter.operators
        ]
        rules += [(r"%s" % b, 0, self.STYLES["brace"]) for b in CHighlighter.braces]
        rules += [(r"%s" % m, 0, self.STYLES["macro"]) for m in CHighlighter.macros]

        rules += [
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.STYLES["string"]),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.STYLES["string"]),
            (r"\b[+-]?[0-9]+[lL]?\b", 0, self.STYLES["numbers"]),
            (r"\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b", 0, self.STYLES["numbers"]),
            (
                r"\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b",
                0,
                self.STYLES["numbers"],
            ),
            (r"//[^\n]*", 0, self.STYLES["comment"]),
        ]

        self.rules = [
            (QRegularExpression(pat), index, fmt) for (pat, index, fmt) in rules
        ]

    def highlightBlock(self, text: str):
        for expression, nth, fm in self.rules:
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), fm)

        self.setCurrentBlockState(0)

        self.match_multiline(text, *self.multiline_comment)

    def match_multiline(
        self,
        text: str,
        delimiter_start: QRegularExpression,
        delimiter_end: QRegularExpression,
        in_state,
        style,
    ):
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = delimiter_start.match(text, 0).capturedStart()

        while start_index >= 0:
            match = delimiter_end.match(text, start_index)
            captured_length = match.capturedLength()
            end_index = match.capturedStart()
            if end_index == -1:
                self.setCurrentBlockState(1)
                length = len(text) - start_index
            else:
                self.setCurrentBlockState(0)
                length = end_index - start_index + captured_length

            self.setFormat(start_index, length, style)
            start_index = delimiter_start.match(
                text, start_index + length
            ).capturedStart()

        if self.currentBlockState() == in_state:
            return True
        else:
            return False
