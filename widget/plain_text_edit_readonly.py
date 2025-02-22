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
# @file        plain_text_edit_readonly.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-22     xqyjlj       initial version
#

from PySide6.QtCore import Qt
from PySide6.QtGui import QInputMethodEvent
from qfluentwidgets import PlainTextEdit


class PlainTextEditReadonly(PlainTextEdit):
    def inputMethodEvent(self, event: QInputMethodEvent):
        if not (self.textInteractionFlags() & Qt.TextInteractionFlag.TextEditable):
            event.ignore()
            return
        super().inputMethodEvent(event)
