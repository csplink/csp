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
# Copyright (C) 2024-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        plain_text_edit_logger.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-21     xqyjlj       initial version
#

import logging

from PySide6.QtGui import QFont
from loguru import logger

# noinspection PyProtectedMember
from loguru._handler import Message

from common import Style
from .plain_text_edit_readonly import PlainTextEditReadonly


class PlainTextEditLogger(PlainTextEditReadonly):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabStopDistance(40)
        self.setReadOnly(True)
        self.setMaximumBlockCount(2000)

        font = QFont()
        font.setFamily("JetBrains Mono")
        font.setPointSize(9)
        font.setWeight(QFont.Weight.Light)
        self.setFont(font)

        Style.PLAIN_TEXT_EDIT_LOGGER.apply(self)

        # {level: <8} |  {name}:{function}:{line} - {message}
        logger.add(self.__callback, level=logging.INFO)  # type: ignore

    def __callback(self, message: Message):
        time = message.record["time"]
        level = message.record["level"].name
        msg = message.record["message"]
        file = message.record["file"]
        line = message.record["line"]
        text = (
            f"{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {file.name}:{line} | {msg}"
        )
        self.appendPlainText(text)
