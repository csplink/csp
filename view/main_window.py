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
# @file        main_window.py
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
from common import Icon
from dialogs import GenCodeDialog


class MenuIndexType(Enum):
    FILE_MENU = 0
    PROJECT_MENU = 1


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    menus = []

    def __init__(self, parent):
        super().__init__(parent)

        self.__initMenu()

        # add buttons
        self.layoutBtn = QHBoxLayout()

        self.btnFile = TransparentPushButton(self.tr("File"), self)
        self.btnFile.clicked.connect(lambda: self.menus[MenuIndexType.FILE_MENU.value].exec(
            self.btnFile.mapToGlobal(QPoint(0, self.btnFile.height())), ani=True))

        self.btnProject = TransparentPushButton(self.tr("Project"), self)
        self.btnProject.clicked.connect(lambda: self.menus[MenuIndexType.PROJECT_MENU.value].exec(
            self.btnProject.mapToGlobal(QPoint(0, self.btnProject.height())), ani=True))

        self.layoutBtn.setContentsMargins(20, 0, 20, 0)
        self.layoutBtn.setSpacing(15)
        self.layoutBtn.addWidget(self.btnFile)
        self.layoutBtn.addWidget(self.btnProject)

        self.layoutHeader = self.hBoxLayout
        self.layoutHeader.insertLayout(4, self.layoutBtn)
        self.layoutHeader.setStretch(6, 0)

    def __initMenu(self):
        self.menus.append(self.__createFileMenu())
        self.menus.append(self.__createProjectMenu())

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

        self.actionGenerate = Action(self.tr('Generate'))
        menu.addAction(self.actionGenerate)

        return menu

    def action_generateTriggered(self):
        dialog = GenCodeDialog(self)
        dialog.exec()


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        barTitle = CustomTitleBar(self)

        self.updateFrameless()
        self.setMicaEffectEnabled(False)
        self.setTitleBar(barTitle)

        self.viewChip = ChipView(self)
        self.viewCode = CodeView(self)

        barTitle.actionGenerate.triggered.connect(lambda: self.__on_generate_clicked())

        self.__initNavigation()
        self.__initWindow()

        # self.showMaximized()

    def __initNavigation(self):
        self.addSubInterface(self.viewChip, Icon.CPU, 'Chip', Icon.CPU)
        btnCode = self.addSubInterface(self.viewCode, Icon.CODE, 'Code', Icon.CODE)
        btnCode.clicked.connect(lambda: self.viewCode.flush())

        self.navigationInterface.addItem(
            routeKey='Generate',
            icon=Icon.GENERATE,
            text=self.tr('Generate'),
            onClick=self.__on_generate_clicked,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.addItem(
            routeKey='Sponsor',
            icon=Icon.MONEY,
            text=self.tr('Sponsor'),
            onClick=self.__on_sponsorKey_clicked,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(SettingView(self), Icon.SETTING, self.tr('Settings'), Icon.SETTING,
                             NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.viewChip.objectName())

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/images/logo.svg'))
        self.setWindowTitle('CSPLink')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def __on_sponsorKey_clicked(self):
        w = MessageBox(
            self.tr('Sponsor'),
            self.tr("""The csplink projects are personal open-source projects, their development need your help.
If you would like to support the development of csplink, you are encouraged to donate!"""), self)
        w.yesButton.setText(self.tr('OK'))
        w.cancelButton.setText(self.tr('Cancel'))

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://xqyjlj.github.io/"))

    def __on_generate_clicked(self):
        dialog = GenCodeDialog(self, True)
        dialog.exec()
