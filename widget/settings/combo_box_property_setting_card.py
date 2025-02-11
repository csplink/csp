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
    currentTextChanged = Signal(str)

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
        self.comboBox = ComboBox(self)

        for v in values:
            self.comboBox.addItem(v)

        self.comboBox.setCurrentText(value)
        self.comboBox.currentTextChanged.connect(self.currentTextChanged)

        self.badge = IconInfoBadge.error(
            icon=Icon.CLOSE_LARGE,
            parent=self.comboBox.parent(),
            target=self.comboBox,
            position=InfoBadgePosition.TOP_RIGHT,
        )
        self.badge.hide()

        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def setStatusInfo(self, error: bool, message: str):
        self.badge.setVisible(error)
        if error:
            self.comboBox.setToolTip(message)
        else:
            self.comboBox.setToolTip("")

    def setSource(self, value: str, values: list[str]):
        self.comboBox.currentTextChanged.disconnect(self.currentTextChanged)

        self.comboBox.clear()

        for v in values:
            self.comboBox.addItem(v)

        self.comboBox.currentTextChanged.connect(self.currentTextChanged)

        text = self.comboBox.currentText()
        self.comboBox.setCurrentText(value)
        if text == value:
            self.currentTextChanged.emit(value)

    def clear(self):
        self.comboBox.clear()
        self.setStatusInfo(False, "")
        self.setContent("")
