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
# @file        main_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import os

from enum import Enum

from PySide6.QtCore import QUrl, QPoint
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QApplication

from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow, RoundMenu, Action,
                            TransparentPushButton)

from .chip_view import ChipView
from .setting_view import SettingView
from .code_view import CodeView
from common import Icon, Coder, PROJECT
from dialogs import GenCodeDialog


class MenuIndex(Enum):
    FILE_MENU = 0
    PROJECT_MENU = 1


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    m_menus = []

    def __init__(self, parent):
        super().__init__(parent)

        self.__initMenu()

        # add buttons
        self.layout_toolButton = QHBoxLayout()

        self.button_file = TransparentPushButton(self.tr("File"), self)
        self.button_file.clicked.connect(lambda: self.m_menus[MenuIndex.FILE_MENU.value].exec(
            self.button_file.mapToGlobal(QPoint(0, self.button_file.height())), ani=True))

        self.button_project = TransparentPushButton(self.tr("Project"), self)
        self.button_project.clicked.connect(lambda: self.m_menus[MenuIndex.PROJECT_MENU.value].exec(
            self.button_project.mapToGlobal(QPoint(0, self.button_project.height())), ani=True))

        self.layout_toolButton.setContentsMargins(20, 0, 20, 0)
        self.layout_toolButton.setSpacing(15)
        self.layout_toolButton.addWidget(self.button_file)
        self.layout_toolButton.addWidget(self.button_project)
        self.hBoxLayout.insertLayout(4, self.layout_toolButton)
        self.hBoxLayout.setStretch(6, 0)

    def __initMenu(self):
        self.m_menus.append(self.__createFileMenu())
        self.m_menus.append(self.__createProjectMenu())

    def __createFileMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        action = Action(self.tr('New'))
        menu.addAction(action)

        action = Action(self.tr('Open'))
        menu.addAction(action)

        action = Action(self.tr('Save'))
        menu.addAction(action)

        return menu

    def __createProjectMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.m_action_generate = Action(self.tr('Generate'))
        menu.addAction(self.m_action_generate)

        return menu

    def action_generateTriggered(self):
        dialog = GenCodeDialog(self)
        dialog.exec()


class MainView(MSFluentWindow):

    def __init__(self):
        super().__init__()

        title_bar = CustomTitleBar(self)

        self.updateFrameless()
        self.setMicaEffectEnabled(False)
        self.setTitleBar(title_bar)

        self.chip_view = ChipView(self)
        self.code_view = CodeView(self)

        title_bar.m_action_generate.triggered.connect(lambda: self.__generateCodeClick())

        self.__initNavigation()
        self.__initWindow()

        self.showMaximized()

    def __initNavigation(self):
        self.addSubInterface(self.chip_view, Icon.CPU, 'Chip', Icon.CPU)
        self.addSubInterface(self.code_view, Icon.CODE, 'Code', Icon.CODE)

        self.navigationInterface.addItem(
            routeKey='Generate',
            icon=Icon.GENERATE,
            text=self.tr('Generate'),
            onClick=self.__generateCodeClick,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.addItem(
            routeKey='Sponsor',
            icon=Icon.MONEY,
            text=self.tr('Sponsor'),
            onClick=self.__showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(SettingView(self), Icon.SETTING, self.tr('Settings'), Icon.SETTING,
                             NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.chip_view.objectName())

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/images/logo.svg'))
        self.setWindowTitle('CSPLink')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def __showMessageBox(self):
        w = MessageBox(
            self.tr('Sponsor'),
            self.tr("""The csplink projects are personal open-source projects, their development need your help.
If you would like to support the development of csplink, you are encouraged to donate!"""), self)
        w.yesButton.setText(self.tr('OK'))
        w.cancelButton.setText(self.tr('Cancel'))

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://xqyjlj.github.io/"))

    def __generateCodeClick(self):
        dialog = GenCodeDialog(self, True)
        dialog.exec()
