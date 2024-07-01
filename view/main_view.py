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

from PyQt5.QtCore import QUrl, QPoint
from PyQt5.QtGui import QIcon, QDesktopServices, QKeySequence
from PyQt5.QtWidgets import QHBoxLayout, QApplication

from qfluentwidgets import (NavigationItemPosition, MessageBox, MSFluentTitleBar, MSFluentWindow, RoundMenu, Action,
                            TransparentPushButton)
from qfluentwidgets import FluentIcon as FIF

from .chip_view import ChipView
from .setting_view import SettingView
from common.icon import Icon


class CustomTitleBar(MSFluentTitleBar):
    """ Title bar with icon and title """

    def __init__(self, parent):
        super().__init__(parent)

        # add buttons
        self.toolButtonLayout = QHBoxLayout()

        self.searchButton = TransparentPushButton(self.tr("File"), self)
        self.searchButton.clicked.connect(
            lambda: self.createMenu(self.searchButton.mapToGlobal(QPoint(0, self.searchButton.height()))))

        self.toolButtonLayout.setContentsMargins(20, 0, 20, 0)
        self.toolButtonLayout.setSpacing(15)
        self.toolButtonLayout.addWidget(self.searchButton)
        self.hBoxLayout.insertLayout(4, self.toolButtonLayout)
        self.hBoxLayout.setStretch(6, 0)

        # # add avatar
        # self.avatar = TransparentDropDownToolButton('resource/shoko.png', self)
        # self.avatar.setIconSize(QSize(26, 26))
        # self.avatar.setFixedHeight(30)
        # self.hBoxLayout.insertWidget(6, self.avatar, 0, Qt.AlignRight)
        # self.hBoxLayout.insertSpacing(8, 20)
    def createMenu(self, pos):
        menu = RoundMenu(parent=self)

        # add actions

        action = Action(FIF.COPY, self.tr('New'))
        action.setShortcut(QKeySequence("Ctrl+N"))
        menu.addAction(action)

        action = Action(FIF.COPY, self.tr('Open'))
        action.setShortcut(QKeySequence("Ctrl+O"))
        menu.addAction(action)

        action = Action(FIF.COPY, self.tr('Save'))
        action.setShortcut(QKeySequence("Ctrl+S"))
        menu.addAction(action)

        # # add sub menu
        # submenu = RoundMenu(self.tr("Add to"), self)
        # submenu.setIcon(FIF.ADD)
        # submenu.addActions([
        #     Action(FIF.VIDEO, self.tr('Video')),
        #     Action(FIF.MUSIC, self.tr('Music')),
        # ])
        # menu.addMenu(submenu)

        # # add actions
        # menu.addActions([Action(FIF.PASTE, self.tr('Paste')), Action(FIF.CANCEL, self.tr('Undo'))])

        # # add separator
        # menu.addSeparator()
        # menu.addAction(Action(self.tr('Select all')))

        # # insert actions
        # menu.insertAction(menu.actions()[-1], Action(FIF.SETTING, self.tr('Settings')))
        # menu.insertActions(menu.actions()[-1],
        #                    [Action(FIF.HELP, self.tr('Help')),
        #                     Action(FIF.FEEDBACK, self.tr('Feedback'))])

        menu.exec(pos, ani=True)


class MainView(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.updateFrameless()

        self.setMicaEffectEnabled(False)
        self.setTitleBar(CustomTitleBar(self))

        # create sub interface
        self.ChipView = ChipView(self)

        # self.mainWidget = QSplitter(self)
        # self.mainWidget.setOrientation(Qt.Orientation.Vertical)
        # self.hBoxLayout.replaceWidget(self.stackedWidget, self.mainWidget)
        # self.mainWidget.addWidget(self.stackedWidget)
        # self.mainWidget.addWidget(QWidget(self))

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.ChipView, Icon.CPU, 'Chip', Icon.CPU)

        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text=self.tr('Help'),
            onClick=self.showMessageBox,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.addSubInterface(SettingView(self), FIF.SETTING, self.tr('Settings'), FIF.SETTING,
                             NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.ChipView.objectName())

    def initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/images/logo.svg'))
        self.setWindowTitle('CSPLink')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def showMessageBox(self):
        w = MessageBox('支持作者🥰', '个人开发不易，如果这个项目帮助到了您，可以考虑请作者喝一瓶快乐水🥤。您的支持就是作者开发和维护项目的动力🚀', self)
        w.yesButton.setText('来啦老弟')
        w.cancelButton.setText('下次一定')

        if w.exec():
            QDesktopServices.openUrl(QUrl("https://afdian.net/a/zhiyiYo"))
