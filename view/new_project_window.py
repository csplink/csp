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

import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from qfluentwidgets import (PushButton, TabCloseButtonDisplayMode, FluentIconBase, MSFluentWindow, TextEdit)

from common import SETTINGS, Icon
from .ui.new_project_view_ui import Ui_NewProjectView


class FeatureView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.Icon = None
        self.mainVLayout = QVBoxLayout(self)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.infoHLayout = QHBoxLayout()

        self.textBrowser = TextEdit(self)
        self.textBrowser.setReadOnly(True)
    
        self.mainVLayout.addLayout(self.infoHLayout)
        self.mainVLayout.addWidget(self.textBrowser)


class NewProjectView(Ui_NewProjectView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.tabBar.setAddButtonVisible(False)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.NEVER)

        self.createBtn = PushButton(self.tr('Create'), self)
        self.btnGroupHorizontalLayout.addWidget(self.createBtn, 0, Qt.AlignmentFlag.AlignRight)

        self.treeView.header().setVisible(False)

        self.mainSplitter.setSizes([100, 600])
        self.mainSplitter.setCollapsible(0, False)
        self.mainSplitter.setCollapsible(1, False)
        self.socSplitter.setSizes([200, 100])
        self.socSplitter.setCollapsible(0, False)
        self.socSplitter.setCollapsible(1, False)

        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setSortingEnabled(True)

        self.featureView = FeatureView(self)

        self.addSubInterface(self.featureView, Icon.FOLDER, self.tr('Feature'))

    def addSubInterface(self, interface: QWidget, icon: FluentIconBase, text: str):
        self.stackedWidget.addWidget(interface)
        self.tabBar.addTab(routeKey=interface.objectName(),
                           text=text,
                           icon=icon,
                           onClick=lambda: self.stackedWidget.setCurrentWidget(interface))


class NewProjectWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.navigationInterface.hide()
        self.stackedWidget.hide()

        self.view = NewProjectView()
        self.hBoxLayout.addWidget(self.view)

        self.__initWindow()
        self.showMaximized()

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg")))
        self.setWindowTitle('CSPLink')

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
