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
from PySide6.QtCore import Qt, QCoreApplication, Signal
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (ScrollArea, ExpandLayout, ExpandGroupSettingCard)

from common import Style, Icon, PACKAGE


class VersionInfoWidget(QWidget):
    textChanged = Signal(str)

    def __init__(self, version: str, path: str | None, value: str, content=None, validator=None, parent=None):
        super().__init__(parent=parent)
        self.versionLabel = QLabel(version, self)
        self.pathLabel = QLabel(path or '', self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.pathLabel.hide()

        self.setFixedHeight(70 if content else 50)

        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(16, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.versionLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.pathLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)


class PackageView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PackageView")

        # setting label
        self.settingLabel = QLabel(QCoreApplication.translate("PackageView", "System Setting"), self)
        self.settingLabel.setObjectName('settingLabel')
        self.settingLabel.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widgetScroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)

        self.expandLayout = ExpandLayout(self.widgetScroll)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)

        groups = self.__createGroups("toolchains")
        for group in groups:
            self.expandLayout.addWidget(group)

        self.enableTransparentBackground()

        Style.PACKAGE_VIEW.apply(self)

    def __createGroups(self, kind: str):
        groups = []
        package = PACKAGE.origin.get(kind, {})
        for k, v in package.items():
            group = ExpandGroupSettingCard(Icon.FOLDER.icon(), k, "", self.widgetScroll)
            for version, path in v.items():
                info = VersionInfoSettingCard(Icon.FOLDER, version, "", path, group)
                group.addGroupWidget(info)
            groups.append(group)
        return groups
