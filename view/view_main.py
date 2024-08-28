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
# @file        view_main.py
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

from .view_chip import view_chip
from .view_setting import view_setting
from .view_code import view_code
from common import Icon, Coder, PROJECT
from dialogs import GenCodeDialog


class menu_index_type(Enum):
    FILE_MENU = 0
    PROJECT_MENU = 1


class custom_title_bar(MSFluentTitleBar):
    """ Title bar with icon and title """

    m_menus = []

    def __init__(self, parent):
        super().__init__(parent)

        self.__init_menu()

        # add buttons
        self.layout_btn = QHBoxLayout()

        self.btn_file = TransparentPushButton(self.tr("File"), self)
        self.btn_file.clicked.connect(lambda: self.m_menus[menu_index_type.FILE_MENU.value].exec(
            self.btn_file.mapToGlobal(QPoint(0, self.btn_file.height())), ani=True))

        self.btn_project = TransparentPushButton(self.tr("Project"), self)
        self.btn_project.clicked.connect(lambda: self.m_menus[menu_index_type.PROJECT_MENU.value].exec(
            self.btn_project.mapToGlobal(QPoint(0, self.btn_project.height())), ani=True))

        self.layout_btn.setContentsMargins(20, 0, 20, 0)
        self.layout_btn.setSpacing(15)
        self.layout_btn.addWidget(self.btn_file)
        self.layout_btn.addWidget(self.btn_project)

        self.layout_header = self.hBoxLayout
        self.layout_header.insertLayout(4, self.layout_btn)
        self.layout_header.setStretch(6, 0)

    def __init_menu(self):
        self.m_menus.append(self.__create_file_menu())
        self.m_menus.append(self.__create_project_menu())

    def __create_file_menu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        action = Action(self.tr('New'))
        menu.addAction(action)

        action = Action(self.tr('Open'))
        menu.addAction(action)

        action = Action(self.tr('Save'))
        menu.addAction(action)

        return menu

    def __create_project_menu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.m_action_generate = Action(self.tr('Generate'))
        menu.addAction(self.m_action_generate)

        return menu

    def action_generateTriggered(self):
        dialog = GenCodeDialog(self)
        dialog.exec()


class view_main(MSFluentWindow):

    def __init__(self):
        super().__init__()

        title_bar = custom_title_bar(self)

        self.updateFrameless()
        self.setMicaEffectEnabled(False)
        self.setTitleBar(title_bar)

        self.view_chip = view_chip(self)
        self.view_code = view_code(self)

        title_bar.m_action_generate.triggered.connect(lambda: self.__generateCodeClick())

        self.__init_navigation()
        self.__init_window()

        # self.showMaximized()

    def __init_navigation(self):
        self.addSubInterface(self.view_chip, Icon.CPU, 'Chip', Icon.CPU)
        code_btn = self.addSubInterface(self.view_code, Icon.CODE, 'Code', Icon.CODE)
        code_btn.clicked.connect(lambda: self.view_code.flush())

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
        self.addSubInterface(view_setting(self), Icon.SETTING, self.tr('Settings'), Icon.SETTING,
                             NavigationItemPosition.BOTTOM)

        self.navigationInterface.setCurrentItem(self.view_chip.objectName())

    def __init_window(self):
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
