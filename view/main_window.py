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

from PySide6.QtCore import QUrl, QPoint, QSize, QEventLoop, QTimer
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QApplication

from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow, RoundMenu, Action,
                            TransparentPushButton, SplashScreen)

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

        self.generateAction = Action(self.tr('Generate'))
        menu.addAction(self.generateAction)

        return menu

    def action_generateTriggered(self):
        dialog = GenCodeDialog(self)
        dialog.exec()


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.__initWindow()

        self.chipView = ChipView(self)

        # ugly, because when opengl is created, the window will automatically hide
        self.show()
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)  # splashScreen show at least 3s
        QApplication.processEvents()

        self.codeView = CodeView(self)
        self.settingView = SettingView(self)

        self.__initNavigation()

        self.barTitle.generateAction.triggered.connect(lambda: self.__on_generate_clicked())

        # loop.exec()
        self.splashScreen.finish()

        # self.showMaximized()

    def __initNavigation(self):
        self.addSubInterface(self.chipView, Icon.CPU, 'Chip', Icon.CPU)
        btnCode = self.addSubInterface(self.codeView, Icon.CODE, 'Code', Icon.CODE)
        btnCode.clicked.connect(lambda: self.codeView.flush())

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
        self.addSubInterface(self.settingView, Icon.SETTING, self.tr('Settings'), Icon.SETTING,
                             NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.settingView.objectName())
        self.switchTo(self.settingView)

    def __initWindow(self):
        self.barTitle = CustomTitleBar(self)
        self.setTitleBar(self.barTitle)

        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/images/logo.svg'))
        self.setWindowTitle('CSPLink')

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

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
