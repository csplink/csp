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

from PySide6.QtCore import QUrl, QPoint, QSize, QEventLoop, QTimer, Qt
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QHBoxLayout, QApplication, QMessageBox, QWidget
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow, RoundMenu, Action,
                            TransparentPushButton, SplashScreen, FluentIconBase, NavigationBarPushButton)

from common import Icon, SETTINGS, SIGNAL_BUS, PROJECT, Coder
from .clock_tree_view import ClockTreeView
from .code_view import CodeView
from .package_view import PackageView
from .setting_view import SettingView
from .soc_view import SocView


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # add buttons
        self.btnLayout = QHBoxLayout()

        # ----------------------------------------------------------------------
        self.fileBtn = TransparentPushButton(self.tr("File"), self)
        self.fileMenu = self.__createFileMenu()
        self.fileBtn.clicked.connect(
            lambda: self.fileMenu.exec(self.fileBtn.mapToGlobal(QPoint(0, self.fileBtn.height())), ani=True))
        # ----------------------------------------------------------------------
        self.projectBtn = TransparentPushButton(self.tr("Project"), self)
        self.projectMenu = self.__createProjectMenu()
        self.projectBtn.clicked.connect(
            lambda: self.projectMenu.exec(self.projectBtn.mapToGlobal(QPoint(0, self.projectBtn.height())), ani=True))
        # ----------------------------------------------------------------------
        self.helpBtn = TransparentPushButton(self.tr("Help"), self)
        self.helpMenu = self.__createHelpMenu()
        self.helpBtn.clicked.connect(
            lambda: self.helpMenu.exec(self.helpBtn.mapToGlobal(QPoint(0, self.helpBtn.height())), ani=True))
        # ----------------------------------------------------------------------
        self.btnLayout.setContentsMargins(20, 0, 20, 0)
        self.btnLayout.setSpacing(15)
        self.btnLayout.addWidget(self.fileBtn)
        self.btnLayout.addWidget(self.projectBtn)
        self.btnLayout.addWidget(self.helpBtn)

        self.layoutHeader = self.hBoxLayout
        self.layoutHeader.insertLayout(4, self.btnLayout)
        self.layoutHeader.setStretch(6, 0)

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

    def __createHelpMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.aboutQtAction = Action(self.tr('About Qt'))
        self.aboutAction = Action(self.tr('About'))
        self.openSourceLicenseAction = Action(self.tr('Open Source License'))
        menu.addAction(self.aboutQtAction)
        menu.addAction(self.aboutAction)
        menu.addSeparator()
        menu.addAction(self.openSourceLicenseAction)

        return menu

    def action_generateTriggered(self):
        pass


class MainWindow(MSFluentWindow):
    __viewMap = {}

    def __init__(self):
        super().__init__()

        self.__initWindow()

        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)  # splashScreen show at least 3s
        QApplication.processEvents()

        self.socView = SocView(self)
        self.clockTreeView = ClockTreeView(self)

        # ugly, because when opengl is created, the window will automatically hide
        self.show()

        self.codeView = CodeView(self)
        self.packageView = PackageView(self)
        self.settingView = SettingView(self)

        self.__initNavigation()

        self.barTitle.generateAction.triggered.connect(lambda: self.__on_generate_clicked())
        self.barTitle.aboutQtAction.triggered.connect(lambda: QMessageBox.aboutQt(self.window(), self.tr('About Qt')))
        SIGNAL_BUS.navigationRequested.connect(self.__on_x_navigationRequested, Qt.ConnectionType.QueuedConnection)
        self.stackedWidget.currentChanged.connect(self.__on_stackedWidget_currentChanged,
                                                  Qt.ConnectionType.QueuedConnection)

        # loop.exec()
        self.splashScreen.finish()

        # self.showMaximized()

    def __initNavigation(self):
        self.__addView(self.socView, Icon.CPU, self.tr('SOC'), Icon.CPU)
        self.__addView(self.clockTreeView, Icon.TIME, self.tr('Clock'), Icon.TIME)
        self.__addView(self.codeView, Icon.CODE, self.tr('Code'), Icon.CODE)

        self.navigationInterface.addItem(routeKey='Generate', icon=Icon.FOLDER_TRANSFER, text=self.tr('Generate'),
                                         onClick=self.__on_generate_clicked,
                                         selectable=False,
                                         position=NavigationItemPosition.BOTTOM)

        self.navigationInterface.addItem(routeKey='Sponsor', icon=Icon.MONEY, text=self.tr('Sponsor'),
                                         onClick=self.__on_sponsorKey_clicked,
                                         selectable=False,
                                         position=NavigationItemPosition.BOTTOM)

        self.__addView(self.packageView, Icon.BOOK_SHELF, self.tr('Package'), Icon.BOOK_SHELF,
                       NavigationItemPosition.BOTTOM)
        self.__addView(self.settingView, Icon.SETTING, self.tr('Settings'), Icon.SETTING, NavigationItemPosition.BOTTOM)
        self.navigationInterface.setCurrentItem(self.socView.objectName())

    def __initWindow(self):
        self.barTitle = CustomTitleBar(self)
        self.setTitleBar(self.barTitle)

        self.resize(1100, 750)
        self.setWindowIcon(QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg")))
        self.setWindowTitle('CSPLink')

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        # noinspection DuplicatedCode
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()

    def __addView(self, interface: QWidget, icon: FluentIconBase, text: str,
                  selectedIcon=None, position=NavigationItemPosition.TOP,
                  isTransparent=False) -> NavigationBarPushButton:
        self.__viewMap[interface.objectName()] = interface
        return self.addSubInterface(interface, icon, text, selectedIcon, position, isTransparent)

    def __on_sponsorKey_clicked(self):
        message = MessageBox(self.tr('Sponsor'),
                             self.tr("""The csplink projects are personal open-source projects, their development need your help.
If you would like to support the development of csplink, you are encouraged to donate!"""), self)
        message.yesButton.setText(self.tr('OK'))
        message.cancelButton.setText(self.tr('Cancel'))

        if message.exec():
            QDesktopServices.openUrl(QUrl(SETTINGS.AUTHOR_BLOG_URL))

    def __on_generate_clicked(self):
        if not PROJECT.isGenerateSettingValid():
            title = self.tr('Error')
            content = self.tr("The coder settings is invalid. Please check it.")
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.cancelButton.setDisabled(True)
            message.raise_()
            message.exec()
            SIGNAL_BUS.navigationRequested.emit('SettingView', 'GenerateSettingView')
            return

        coder = Coder()
        coder.generate()

    def __on_x_navigationRequested(self, routeKey: str, subKey: str):
        if routeKey in self.navigationInterface.items.keys():
            self.switchTo(self.__viewMap[routeKey])
            self.navigationInterface.setCurrentItem(routeKey)
            if routeKey == 'SettingView' and len(subKey) > 0:
                self.settingView.switchTo(subKey)

    def __on_stackedWidget_currentChanged(self, index: int):
        view = self.stackedWidget.widget(index)
        if view == self.codeView:
            self.codeView.flush()
        elif view == self.packageView:
            self.packageView.flush()
