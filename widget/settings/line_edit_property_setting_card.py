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
# from PySide6.QtWidgets import QWidget

from qfluentwidgets import (FluentIconBase, SettingCard, LineEdit, IconInfoBadge, InfoBadgePosition, ToolTipFilter)

from common import Icon


class LineEditPropertySettingCard(SettingCard):

    textChanged = Signal(str)

    def __init__(self, icon: FluentIconBase, title: str, value: str, content=None, validator=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.edit = LineEdit(self)
        if validator != None:
            self.edit.setValidator(QRegularExpressionValidator(QRegularExpression(validator)))
        self.edit.setText(value)
        self.edit.textChanged.connect(self.textChanged)

        self.badge = IconInfoBadge.error(icon=Icon.CLOSE_LARGE,
                                         parent=self.edit.parent(),
                                         target=self.edit,
                                         position=InfoBadgePosition.TOP_RIGHT)
        self.badge.hide()

        self.hBoxLayout.addWidget(self.edit, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

    def setStatusInfo(self, error: bool, message: str):
        self.badge.setVisible(error)
        if error:
            self.edit.setToolTip(message)
        else:
            self.edit.setToolTip("")
