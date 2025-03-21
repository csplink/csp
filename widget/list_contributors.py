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

from PySide6.QtCore import Qt, QPoint, QObject, QEvent, QUrl, QRect
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import (
    RoundMenu,
    FlowLayout,
    AvatarWidget,
    Action,
    CaptionLabel,
    HyperlinkLabel,
    isDarkTheme,
    ScrollArea,
)

from common import SETTINGS, Icon, Contributor, ContributorType

AVATAR_SIZE = 32
CONTRIBUTORS_DIR = os.path.dirname(SETTINGS.CONTRIBUTORS_FILE)


class CardProfile(QWidget):
    """Profile card"""

    def __init__(self, avatar_path: str, name: str, url: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatar_path, self)
        self.name_label = HyperlinkLabel(QUrl(url), name, self)
        self.url_label = CaptionLabel(url, self)

        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.url_label.setStyleSheet("QLabel{color: " + color.name() + "}")

        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.name_label.move(64, 13)
        self.url_label.move(64, 32)


class ListContributors(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # ----------------------------------------------------------------------
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = ScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget_contents = QWidget()
        self.scroll_area_widget_contents.setGeometry(QRect(0, 0, 398, 298))
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.v_layout.addWidget(self.scroll_area)
        # ----------------------------------------------------------------------

        self.flow_widget = QWidget(self)
        self.flow_layout = FlowLayout(self.flow_widget, needAni=True)
        self.flow_layout.setContentsMargins(0, 0, 0, 0)
        self.flow_layout.setVerticalSpacing(20)
        self.flow_layout.setHorizontalSpacing(10)
        self.scroll_area.setWidget(self.flow_widget)
        self.scroll_area.enableTransparentBackground()

        contributors = Contributor().contributors()

        for contributor in contributors:
            label = AvatarWidget(f"{CONTRIBUTORS_DIR}/{contributor.avatar}", self)
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.installEventFilter(self)
            label.setRadius(AVATAR_SIZE // 2)
            label.setProperty("info", contributor)
            self.flow_layout.addWidget(label)

    def create_custom_widget_menu(self, contributor: ContributorType, pos: QPoint):
        menu = RoundMenu(parent=self)
        card = CardProfile(
            f"{CONTRIBUTORS_DIR}/{contributor.avatar}",
            contributor.name,
            contributor.html_url,
            menu,
        )
        menu.addWidget(card, selectable=False)

        menu.addSeparator()
        action = Action(Icon.GITHUB, self.tr("Open Github Url"))
        action.setProperty("url", contributor.html_url)
        action.triggered.connect(self.__on_github_action_triggered)
        menu.addAction(action)
        menu.exec(pos)

    def __on_github_action_triggered(self):
        QDesktopServices.openUrl(QUrl(self.sender().property("url")))

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, AvatarWidget):
            if event.type() == QEvent.Type.MouseButtonRelease:
                self.create_custom_widget_menu(
                    watched.property("info"),
                    watched.mapToGlobal(QPoint(watched.width(), 0)),
                )
        return super().eventFilter(watched, event)
