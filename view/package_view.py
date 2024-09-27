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

import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QCoreApplication, Signal, QPoint
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (ScrollArea, ExpandLayout, ExpandGroupSettingCard, PushButton, TransparentToolButton,
                            IconInfoBadge, InfoBadgePosition, RoundMenu, Action)

from common import Style, Icon, PACKAGE


class VersionInfoWidget(QWidget):
    textChanged = Signal(str)

    def __init__(self, version: str, path: str | None, date: str | None, existed: bool, parent=None):
        super().__init__(parent=parent)
        self.versionLabel = QLabel(version, self)
        self.pathLabel = QLabel(path or '', self)
        if path is not None:
            self.pathLabel.setToolTip(path)
        self.pathLabel.setObjectName('pathLabel')
        self.dateLabel = QLabel(date or '', self)
        self.detailBtn = PushButton(QCoreApplication.translate("VersionInfoWidget", "Detail"), self)
        self.menuBtn = TransparentToolButton(Icon.MORE, self)
        self.menuBtn.clicked.connect(lambda: self.__createMenu().exec(
            self.menuBtn.mapToGlobal(QPoint(0, self.menuBtn.height())), ani=True))
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not path:
            self.pathLabel.hide()

        self.setFixedHeight(70 if path else 50)

        Style.PACKAGE_VIEW.apply(self)

        path = self.pathLabel.fontMetrics().elidedText(path, Qt.TextElideMode.ElideRight, 600)
        self.pathLabel.setText(path)

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

        self.hBoxLayout.addWidget(self.dateLabel, 1, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.addWidget(self.detailBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.hBoxLayout.addWidget(self.menuBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.badge = IconInfoBadge.error(icon=Icon.CLOSE_LARGE,
                                         parent=self.pathLabel.parent(),
                                         target=self.pathLabel,
                                         position=InfoBadgePosition.TOP_RIGHT)
        if not existed:
            self.detailBtn.hide()
            self.dateLabel.hide()
            self.menuBtn.hide()
            self.setToolTip(QCoreApplication.translate('VersionInfoWidget', 'The package not found'))
        else:
            self.badge.hide()

    def __createMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.uninstallAction = Action(Icon.UNINSTALL, QCoreApplication.translate("VersionInfoWidget", 'Uninstall'))
        menu.addAction(self.uninstallAction)

        return menu


class PackageView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PackageView")

        # setting label
        self.titleLabel = QLabel(QCoreApplication.translate("PackageView", "Package"), self)
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.move(36, 30)

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
        package = PACKAGE.index.origin.get(kind, {})
        for k, v in package.items():
            group = ExpandGroupSettingCard(Icon.FOLDER.icon(), k, "", self.widgetScroll)
            for version, path in v.items():
                pdsc = PACKAGE.getPackageDescription(path)
                if pdsc is not None:
                    path_info = Path(path)
                    time = datetime.datetime.fromtimestamp(path_info.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    time = QCoreApplication.translate("PackageView", "Install time: %1").replace("%1", time)
                    info = VersionInfoWidget(version, path, time, True, group)
                else:
                    info = VersionInfoWidget(version, path, None, False, group)
                group.addGroupWidget(info)
            groups.append(group)
        return groups
