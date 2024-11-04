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
# @file        list_contributors.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-02     xqyjlj       initial version
#

import os

from PySide6.QtCore import Qt, QPoint, QObject, QEvent, QUrl
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QWidget
from qfluentwidgets import (RoundMenu, FlowLayout, AvatarWidget, Action, CaptionLabel, HyperlinkLabel, isDarkTheme)

from common import SETTINGS, Icon, Contributor, ContributorType
from .ui.list_contributors_ui import Ui_ListContributors

AVATAR_SIZE = 32
CONTRIBUTORS_DIR = os.path.dirname(SETTINGS.CONTRIBUTORS_FILE)


class CardProfile(QWidget):
    """ Profile card """

    def __init__(self, avatarPath: str, name: str, url: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = HyperlinkLabel(QUrl(url), name, self)
        self.urlLabel = CaptionLabel(url, self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.urlLabel.setStyleSheet('QLabel{color: ' + color.name() + '}')

        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.urlLabel.move(64, 32)


class ListContributors(Ui_ListContributors, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.flowWidget = QWidget(self)
        self.flowLayout = FlowLayout(self.flowWidget, needAni=True)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setVerticalSpacing(20)
        self.flowLayout.setHorizontalSpacing(10)
        self.scrollArea.setWidget(self.flowWidget)
        self.scrollArea.enableTransparentBackground()

        contributors = Contributor().contributors

        for contributor in contributors:
            label = AvatarWidget(f'{CONTRIBUTORS_DIR}/{contributor.avatar}', self)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.installEventFilter(self)
            label.setRadius(AVATAR_SIZE // 2)
            label.setProperty("info", contributor)
            self.flowLayout.addWidget(label)

    def createCustomWidgetMenu(self, contributor: ContributorType, pos: QPoint):
        menu = RoundMenu(parent=self)
        card = CardProfile(f'{CONTRIBUTORS_DIR}/{contributor.avatar}', contributor.name, contributor.htmlUrl, menu)
        menu.addWidget(card, selectable=False)

        menu.addSeparator()
        action = Action(Icon.GITHUB, self.tr('Open Github Url'))
        action.setProperty("url", contributor.htmlUrl)
        action.triggered.connect(self.__on_githubAction_triggered)
        menu.addAction(action)
        menu.exec(pos)

    def __on_githubAction_triggered(self):
        QDesktopServices.openUrl(QUrl(self.sender().property("url")))

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, AvatarWidget):
            if event.type() == QEvent.Type.MouseButtonRelease:
                self.createCustomWidgetMenu(watched.property("info"), watched.mapToGlobal(QPoint(watched.width(), 0)))
        return super().eventFilter(watched, event)
