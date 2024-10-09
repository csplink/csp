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

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QBoxLayout, QFileDialog
from qfluentwidgets import (PushButton, MSFluentWindow)

from common import SETTINGS, PROJECT
from widget import ListContributors
from .main_window import MainWindow
from .ui.startup_view_ui import Ui_StartupView


class StartupView(Ui_StartupView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__initCardCommand()
        self.__initContributors()
        self.__initProjectList()
        self.__initMore()

    def __initCardCommand(self):
        self.cardCommand.setTitle(self.tr("I Need To:"))
        self.newSocProjectBtn = PushButton(self.tr("New SOC Project"))
        self.openProjectBtn = PushButton(self.tr("Open Project"))
        self.cardCommand.viewLayout.setContentsMargins(30, 30, 30, 30)
        self.cardCommand.viewLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.cardCommand.viewLayout.addWidget(self.newSocProjectBtn)
        self.cardCommand.viewLayout.addWidget(self.openProjectBtn)

    def __initContributors(self):
        self.cardContributors.setTitle(self.tr("Contributors"))
        self.listContributors = ListContributors(self)
        self.cardContributors.viewLayout.addWidget(self.listContributors)

    def __initProjectList(self):
        self.cardProjectList.setTitle(self.tr("Recent Opened Projects"))

    def __initMore(self):
        self.cardMore.setTitle(self.tr("More"))


class StartupWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.navigationInterface.hide()
        self.stackedWidget.hide()

        self.view = StartupView()
        self.hBoxLayout.addWidget(self.view)

        self.view.newSocProjectBtn.pressed.connect(self.__on_newSocProjectBtn_pressed)
        self.view.openProjectBtn.pressed.connect(self.__on_openProjectBtn_pressed)

        self.__initWindow()

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg")))
        self.setWindowTitle('CSPLink')

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def __on_newSocProjectBtn_pressed(self):
        pass

    def __on_openProjectBtn_pressed(self):
        path, ok = QFileDialog.getOpenFileName(self,
                                               self.tr('Open CSP project file'),
                                               SETTINGS.lastPackageFileFolder.value,
                                               self.tr('CSP project file (*.csp)'))
        if ok:
            SETTINGS.set(SETTINGS.lastPackageFileFolder, os.path.dirname(path))
            PROJECT.path = path
            if PROJECT.valid:
                self.deleteLater()
                self.hide()
                window = MainWindow()
                window.updateFrameless()
                window.show()
