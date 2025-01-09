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
from PySide6.QtGui import QIcon, QDesktopServices, QCloseEvent
from PySide6.QtWidgets import QHBoxLayout, QApplication, QWidget, QSplitter, QVBoxLayout, QMessageBox
from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow, RoundMenu, Action,
                            TransparentPushButton, SplashScreen, FluentIconBase, NavigationBarPushButton, BodyLabel,
                            getFont, FluentStyleSheet, Pivot)

from common import Icon, SETTINGS, SIGNAL_BUS, PROJECT, Coder
from dialogs import PackageInstallDialog
from view import ClockTreeView, CodeView, PackageView, SettingView, SocView
from widget import StackedWidget, PlainTextEditLogger


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # add buttons
        self.btnLayout = QHBoxLayout()

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
        self.packageBtn = TransparentPushButton(self.tr("Package"), self)
        self.packageMenu = self.__createPackageMenu()
        self.packageBtn.clicked.connect(
            lambda: self.packageMenu.exec(self.packageBtn.mapToGlobal(QPoint(0, self.packageBtn.height())), ani=True))
        # ----------------------------------------------------------------------
        self.btnLayout.setContentsMargins(20, 0, 20, 0)
        self.btnLayout.setSpacing(15)

        self.btnLayout.addWidget(self.projectBtn)
        self.btnLayout.addWidget(self.helpBtn)
        self.btnLayout.addWidget(self.packageBtn)

        self.layoutHeader = self.hBoxLayout
        self.layoutHeader.insertLayout(4, self.btnLayout)

        self.projectLabel = BodyLabel(self)
        self.projectLabel.setFont(getFont(16))
        self.projectLabel.setText(PROJECT.title())
        PROJECT.titleChanged.connect(lambda s: self.projectLabel.setText(s))

        self.hBoxLayout.insertWidget(5, self.projectLabel, 100,
                                     Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.layoutHeader.setStretch(6, 0)

    def __createProjectMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        # self.newAction = Action(self.tr('New'))
        # self.newAction.setShortcut("Ctrl+N")
        # menu.addAction(self.newAction)
        #
        # self.openAction = Action(self.tr('Open'))
        # self.openAction.setShortcut("Ctrl+O")
        # menu.addAction(self.openAction)

        self.saveAction = Action(self.tr('Save'))
        # self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(lambda: PROJECT.save())
        menu.addAction(self.saveAction)

        menu.addSeparator()

        self.generateAction = Action(self.tr('Generate'))
        # self.generateAction.setShortcut("Ctrl+G")
        self.generateAction.triggered.connect(lambda: self.generateCode())
        menu.addAction(self.generateAction)

        return menu

    def __createHelpMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.aboutQtAction = Action(self.tr('About Qt'))
        self.aboutQtAction.triggered.connect(lambda: QMessageBox.aboutQt(self.window(), self.tr('About Qt')))
        menu.addAction(self.aboutQtAction)

        self.aboutAction = Action(self.tr('About'))
        menu.addAction(self.aboutAction)

        menu.addSeparator()

        self.openSourceLicenseAction = Action(self.tr('Open Source License'))
        menu.addAction(self.openSourceLicenseAction)

        return menu

    def __createPackageMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.installPackageAction = Action(self.tr('Install'))
        self.installPackageAction.triggered.connect(lambda: PackageInstallDialog(self.window()).exec())
        menu.addAction(self.installPackageAction)

        return menu

    def generateCode(self):
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


class SubTabViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tabBar = Pivot(self)
        self.stackedWidget = StackedWidget(self)

        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.addWidget(self.tabBar, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        # self.tabBar.setTabsClosable(False)
        # self.tabBar.setTabShadowEnabled(False)
        # self.tabBar.setAddButtonVisible(False)
        # self.tabBar.setTabMinimumWidth(30)

    def addSubInterface(self, view: QWidget, text, isTransparent=False):
        if not view.objectName():
            raise ValueError("The object name of `interface` can't be empty string.")
        view.setProperty("isStackedTransparent", isTransparent)
        self.stackedWidget.addWidget(view)

        routeKey = view.objectName()
        item = self.tabBar.addItem(
            routeKey=routeKey,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(view))
        item.setFont(getFont(13))

        if self.stackedWidget.count() == 1:
            self.stackedWidget.currentChanged.connect(self.__on_stackedWidget_currentChanged)
            self.tabBar.setCurrentItem(routeKey)

        self.__updateStackedBackground()

    def __on_stackedWidget_currentChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.tabBar.setCurrentItem(widget.objectName())

        self.__updateStackedBackground()

    def __updateStackedBackground(self):
        isTransparent = self.stackedWidget.currentWidget().property("isStackedTransparent")
        if bool(self.stackedWidget.property("isTransparent")) == isTransparent:
            return

        self.stackedWidget.setProperty("isTransparent", isTransparent)
        self.stackedWidget.setStyle(QApplication.style())


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.__views = {}

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

        self.viewSplitter = QSplitter(Qt.Orientation.Vertical, self)
        self.subTabView = SubTabViewWidget(self.viewSplitter)
        self.plainTextEditLogger = PlainTextEditLogger(self.subTabView)
        self.plainTextEditLogger.setObjectName("plainTextEditLogger")

        old = self.stackedWidget
        old.deleteLater()
        self.stackedWidget = StackedWidget(self.viewSplitter)

        self.__initMainView()
        self.__initNavigation()
        self.__initSubTabView()

        # project --------------------------------------------------------------

        SIGNAL_BUS.navigationRequested.connect(self.__on_x_navigationRequested, Qt.ConnectionType.QueuedConnection)
        self.stackedWidget.currentChanged.connect(self.__on_stackedWidget_currentChanged,
                                                  Qt.ConnectionType.QueuedConnection)

        if SETTINGS.DEBUG:
            self.splashScreen.finish()
        else:
            loop.exec()
            self.splashScreen.finish()
            self.showMaximized()

    def closeEvent(self, event: QCloseEvent):
        if PROJECT.isChanged():
            title = self.tr('Warning')
            content = self.tr("The project {!r} has not been saved yet, do you want to exit?").format(
                PROJECT.project().name)
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.raise_()
            if message.exec():
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def __initNavigation(self):
        self.__addView(self.socView, Icon.CPU, self.tr('SOC'), Icon.CPU)
        self.__addView(self.clockTreeView, Icon.TIME, self.tr('Clock'), Icon.TIME)
        self.__addView(self.codeView, Icon.CODE, self.tr('Code'), Icon.CODE)

        self.navigationInterface.addItem(routeKey='Generate', icon=Icon.FOLDER_TRANSFER, text=self.tr('Generate'),
                                         onClick=lambda: self.titleBar.generateCode(),
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

    def __initMainView(self):
        self.hBoxLayout.removeWidget(self.stackedWidget)
        self.viewSplitter.addWidget(self.stackedWidget)
        self.viewSplitter.addWidget(self.subTabView)
        self.viewSplitter.setSizes([700, 200])
        self.viewSplitter.setCollapsible(0, False)
        self.viewSplitter.setCollapsible(1, False)
        self.hBoxLayout.addWidget(self.viewSplitter, 1)

        FluentStyleSheet.FLUENT_WINDOW.apply(self.stackedWidget)

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

    def __initSubTabView(self):
        self.subTabView.addSubInterface(self.plainTextEditLogger, self.tr('Log'))

    def __addView(self, view: QWidget, icon: FluentIconBase, text: str, selectedIcon=None,
                  position=NavigationItemPosition.TOP, isTransparent=False) -> NavigationBarPushButton:
        self.__views[view.objectName()] = view
        return self.addSubInterface(view, icon, text, selectedIcon, position, isTransparent)

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
            self.switchTo(self.__views[routeKey])
            self.navigationInterface.setCurrentItem(routeKey)
            if routeKey == 'SettingView' and len(subKey) > 0:
                self.settingView.switchTo(subKey)

    def __on_stackedWidget_currentChanged(self, index: int):
        view = self.stackedWidget.widget(index)
        if view == self.codeView:
            self.codeView.flush()
        elif view == self.packageView:
            self.packageView.flush()
