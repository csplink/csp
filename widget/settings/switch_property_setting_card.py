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
# @file        switch_property_setting_card.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-11     xqyjlj       initial version
#

from PySide6.QtCore import Qt, Signal
from qfluentwidgets import (
    FluentIconBase,
    SettingCard,
    SwitchButton,
    IconInfoBadge,
    InfoBadgePosition,
    IndicatorPosition,
)

from common import Icon


# from PySide6.QtGui import QRegularExpressionValidator
# from PySide6.QtWidgets import QWidget


class SwitchPropertySettingCard(SettingCard):
    checkedChanged = Signal(bool)

    def __init__(
        self, icon: FluentIconBase, title: str, value: bool, content=None, parent=None
    ):
        super().__init__(icon, title, content, parent)
        self.switchButton = SwitchButton(self, indicatorPos=IndicatorPosition.RIGHT)
        self.switchButton.setChecked(value)
        self.switchButton.checkedChanged.connect(self.checkedChanged)

        self.badge = IconInfoBadge.error(
            icon=Icon.CLOSE_LARGE,
            parent=self.switchButton.parent(),
            target=self.switchButton,
            position=InfoBadgePosition.TOP_RIGHT,
        )
        self.badge.hide()

        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def setStatusInfo(self, error: bool, message: str):
        self.badge.setVisible(error)
        if error:
            self.switchButton.setToolTip(message)
        else:
            self.switchButton.setToolTip("")

    def clear(self):
        self.setStatusInfo(False, "")
        self.setContent("")
