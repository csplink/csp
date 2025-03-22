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
    checked_changed = Signal(bool)

    def __init__(
        self, icon: FluentIconBase, title: str, value: bool, content=None, parent=None
    ):
        super().__init__(icon, title, content, parent)
        self.switch_button = SwitchButton(self, indicatorPos=IndicatorPosition.RIGHT)
        self.switch_button.setChecked(value)
        self.switch_button.checkedChanged.connect(self.checked_changed)

        self.badge = IconInfoBadge.error(
            icon=Icon.CLOSE_LARGE,
            parent=self.switch_button.parent(),
            target=self.switch_button,
            position=InfoBadgePosition.TOP_RIGHT,
        )
        self.badge.hide()

        self.hBoxLayout.addWidget(self.switch_button, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def set_status_info(self, error: bool, message: str):
        self.badge.setVisible(error)
        if error:
            self.switch_button.setToolTip(message)
        else:
            self.switch_button.setToolTip("")

    def clear(self):
        self.set_status_info(False, "")
        self.setContent("")
