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

from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QApplication, QWidget, QBoxLayout, QFileDialog
from qfluentwidgets import PushButton, MSFluentWindow

from common import SETTINGS, PROJECT
from widget import ListContributors
from .main_window import MainWindow
from .new_project_window import NewProjectWindow
from .ui.startup_view_ui import Ui_StartupView


class StartupView(Ui_StartupView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__init_card_command()
        self.__init_contributors()
        self.__init_project_list()
        self.__init_more()

    def __init_card_command(self):
        self.cardCommand.setTitle(self.tr("I Need To:"))
        self.new_soc_project_btn = PushButton(self.tr("New SOC Project"))
        self.open_project_btn = PushButton(self.tr("Open Project"))
        self.cardCommand.viewLayout.setContentsMargins(30, 30, 30, 30)
        self.cardCommand.viewLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.cardCommand.viewLayout.addWidget(self.new_soc_project_btn)
        self.cardCommand.viewLayout.addWidget(self.open_project_btn)

    def __init_contributors(self):
        self.cardContributors.setTitle(self.tr("Contributors"))
        self.list_contributors = ListContributors(self)
        self.cardContributors.viewLayout.addWidget(self.list_contributors)

    def __init_project_list(self):
        self.cardProjectList.setTitle(self.tr("Recent Opened Projects"))

    def __init_more(self):
        self.cardMore.setTitle(self.tr("More"))


class StartupWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.__main_window = None
        self.__new_project_window = None

        self.navigationInterface.hide()
        self.stackedWidget.hide()

        self.view = StartupView()
        self.hBoxLayout.addWidget(self.view)

        self.view.new_soc_project_btn.pressed.connect(
            self.__on_newSocProjectBtn_pressed
        )
        self.view.open_project_btn.pressed.connect(self.__on_openProjectBtn_pressed)

        self.__init_window()

    def __init_window(self):
        self.resize(1100, 750)
        self.setWindowIcon(
            QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg"))
        )
        self.setWindowTitle("CSPLink")

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def __on_newSocProjectBtn_pressed(self):
        self.__new_project_window = NewProjectWindow()
        self.__new_project_window.updateFrameless()
        self.__new_project_window.setAttribute(Qt.WidgetAttribute.WA_ShowModal, True)
        self.__new_project_window.show()
        self.__new_project_window.succeed.connect(self.__on_newProjectWindow_succeed)

    def __on_newProjectWindow_succeed(self):
        self.__new_project_window = None
        self.deleteLater()
        self.hide()

    def __on_openProjectBtn_pressed(self):
        path, ok = QFileDialog.getOpenFileName(
            self,
            self.tr("Open CSP project file"),
            SETTINGS.last_package_file_folder.value,
            self.tr("CSP project file (*.csp)"),
        )
        if ok:
            SETTINGS.set(SETTINGS.last_package_file_folder, os.path.dirname(path))
            PROJECT.set_path(path)
            if PROJECT.valid():
                self.deleteLater()
                self.hide()
                self.__main_window = MainWindow()
                self.__main_window.updateFrameless()
                self.__main_window.setAttribute(Qt.WidgetAttribute.WA_ShowModal, True)
                self.__main_window.show()
