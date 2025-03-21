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
# @file        combo_box_property_setting_card.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-10     xqyjlj       initial version
#

from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    FluentIconBase,
    SettingCard,
    ComboBox,
    IconInfoBadge,
    InfoBadgePosition,
)

from common import Icon


class ComboBoxPropertySettingCard(SettingCard):
    current_text_changed = Signal(str)

    def __init__(
        self,
        icon: FluentIconBase,
        title: str,
        value: str,
        values: list,
        content=None,
        parent=None,
    ):
        super().__init__(icon, title, content, parent)
        self.combo_box = ComboBox(self)

        for v in values:
            self.combo_box.addItem(v)

        self.combo_box.setCurrentText(value)
        self.combo_box.currentTextChanged.connect(self.current_text_changed)

        self.badge = IconInfoBadge.error(
            icon=Icon.CLOSE_LARGE,
            parent=self.combo_box.parent(),
            target=self.combo_box,
            position=InfoBadgePosition.TOP_RIGHT,
        )
        self.badge.hide()

        self.hBoxLayout.addWidget(self.combo_box, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def set_status_info(self, error: bool, message: str):
        self.badge.setVisible(error)
        if error:
            self.combo_box.setToolTip(message)
        else:
            self.combo_box.setToolTip("")

    def set_source(self, value: str, values: list[str]):
        self.combo_box.currentTextChanged.disconnect(self.current_text_changed)

        self.combo_box.clear()

        for v in values:
            self.combo_box.addItem(v)

        self.combo_box.currentTextChanged.connect(self.current_text_changed)

        text = self.combo_box.currentText()
        self.combo_box.setCurrentText(value)
        if text == value:
            self.current_text_changed.emit(value)

    def clear(self):
        self.combo_box.clear()
        self.set_status_info(False, "")
        self.setContent("")
