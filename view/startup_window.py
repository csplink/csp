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
# @file        startup_window.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-08-28     xqyjlj       initial version
#

import os

from PySide6.QtCore import QStandardPaths
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QApplication, QWidget, QBoxLayout, QHBoxLayout, QFileDialog

from qfluentwidgets import (PushButton, FluentTitleBar)
from qframelesswindow import (FramelessWindow)

from common import SETTINGS, PROJECT

from .ui.ui_startup_view import Ui_StartupView

from widget import ListContributors


class StartupView(Ui_StartupView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__initCardCommand()
        self.__initContributors()
        self.__initProjectList()
        self.__initMore()

    def __initCardCommand(self):
        self.cardCommand.setTitle(self.tr("Command"))
        self.newChipProjectBtn = PushButton(self.tr("New Chip Project"))
        self.openProjectBtn = PushButton(self.tr("Open Project"))
        self.cardCommand.viewLayout.setContentsMargins(30, 30, 30, 30)
        self.cardCommand.viewLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.cardCommand.viewLayout.addWidget(self.newChipProjectBtn)
        self.cardCommand.viewLayout.addWidget(self.openProjectBtn)

        self.newChipProjectBtn.pressed.connect(self.__on_newChipProjectBtn_pressed)
        self.openProjectBtn.pressed.connect(self.__on_openProjectBtn_pressed)

    def __initContributors(self):
        self.cardContributors.setTitle(self.tr("Contributors"))
        self.listContributors = ListContributors(self)
        self.cardContributors.viewLayout.addWidget(self.listContributors)

    def __initProjectList(self):
        self.cardProjectList.setTitle(self.tr("Project List"))

    def __initMore(self):
        self.cardMore.setTitle(self.tr("More"))

    def __on_newChipProjectBtn_pressed(self):
        pass

    def __on_openProjectBtn_pressed(self):
        path, ok = QFileDialog.getOpenFileName(self,
                                               self.tr('Open CSP project file'), SETTINGS.lastOpenProjectFolder.value,
                                               self.tr('CSP project file (*.csp)'))
        if ok:
            SETTINGS.set(SETTINGS.lastOpenProjectFolder, os.path.dirname(path))
            PROJECT.path = path


class StartupWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.view = StartupView()
        self.vBoxLayout.addWidget(self.view)

        self.__initWindow()

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/images/logo.svg'))
        self.setWindowTitle('CSPLink')
        self.titleBar.hBoxLayout.insertSpacing(0, 20)
        self.titleBar.hBoxLayout.insertSpacing(2, 2)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
