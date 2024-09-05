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
# @file        new_project_window.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-05     xqyjlj       initial version
#

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QApplication, QWidget, QBoxLayout, QHBoxLayout

from qfluentwidgets import (PushButton, FluentTitleBar)
from qframelesswindow import (FramelessWindow)

from .ui.ui_new_project_view import Ui_NewProjectView


class NewProjectView(Ui_NewProjectView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class NewProjectWindow(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.view = NewProjectView()
        self.vBoxLayout.addWidget(self.view)

        self.__initWindow()
        self.showMaximized()

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon('resource/images/logo.svg'))
        self.setWindowTitle('CSPLink')
        self.titleBar.hBoxLayout.insertSpacing(0, 20)
        self.titleBar.hBoxLayout.insertSpacing(2, 2)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
