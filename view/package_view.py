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
# @file        package_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-23     xqyjlj       initial version
#
from PySide6.QtCore import Qt, QUrl, QItemSelection
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QTreeWidgetItem

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PushSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea, ComboBoxSettingCard, ExpandLayout, FluentIconBase,
                            CustomColorSettingCard, setTheme, setThemeColor, InfoBar, MessageBox, ToolButton)

from common import (SETTINGS, Style, Icon, PROJECT, PACKAGE)
from utils import converters
from widget import (LineEditPropertySettingCard, ComboBoxPropertySettingCard, SwitchPropertySettingCard,
                    ToolButtonPropertySettingCard)


class PackageView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PackageView")

        # setting label
        self.settingLabel = QLabel(self.tr("System Setting"), self)
        self.settingLabel.setObjectName('settingLabel')
        self.settingLabel.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widgetScroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)

        self.enableTransparentBackground()
