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
# @file        line_edit_property_setting_card.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-10     xqyjlj       initial version
#

from PySide6.QtCore import Qt, QRegularExpression, Signal
from PySide6.QtGui import QRegularExpressionValidator
from qfluentwidgets import (
    FluentIconBase,
    SettingCard,
    LineEdit,
    IconInfoBadge,
    InfoBadgePosition,
)

from common import Icon


# from PySide6.QtWidgets import QWidget


class LineEditPropertySettingCard(SettingCard):
    text_changed = Signal(str)

    def __init__(
        self,
        icon: FluentIconBase,
        title: str,
        value: str,
        content=None,
        validator=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.line_edit = LineEdit(self)
        if validator is not None:
            self.line_edit.setValidator(
                QRegularExpressionValidator(QRegularExpression(validator))
            )
        self.line_edit.setText(value)
        self.line_edit.textChanged.connect(self.text_changed)

        self.badge = IconInfoBadge.error(
            icon=Icon.CLOSE_LARGE,
            parent=self.line_edit.parent(),
            target=self.line_edit,
            position=InfoBadgePosition.TOP_RIGHT,
        )
        self.badge.hide()

        self.hBoxLayout.addWidget(self.line_edit, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def set_status_info(self, error: bool, message: str):
        self.badge.setVisible(error)
        if error:
            self.line_edit.setToolTip(message)
        else:
            self.line_edit.setToolTip("")

    def clear(self):
        self.line_edit.clear()
        self.set_status_info(False, "")
        self.setContent("")
