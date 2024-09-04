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
# @file        view_startup.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-08-28     xqyjlj       initial version
#

from PySide6.QtCore import Qt, Signal, QItemSelection
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QBoxLayout, QFrame, QLabel, QHBoxLayout, QFrame, QSizePolicy

from qfluentwidgets import (PushButton, FlowLayout)
from qframelesswindow import (FramelessWindow, StandardTitleBar)

from .ui.ui_view_startup import Ui_viewStartup

from common import Database
from widget import ListContributors


class ui_viewStartup(Ui_viewStartup, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__initCardCommand()
        self.__initContributors()
        self.__initProjectList()
        self.__initMore()

    def __initCardCommand(self):
        self.cardCommand.setTitle(self.tr("Command"))
        self.btnNewChipProject = PushButton(self.tr("New Chip Project"))
        self.btnOpenProject = PushButton(self.tr("Open Project"))
        self.cardCommand.viewLayout.setContentsMargins(30, 30, 30, 30)
        self.cardCommand.viewLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.cardCommand.viewLayout.addWidget(self.btnNewChipProject)
        self.cardCommand.viewLayout.addWidget(self.btnOpenProject)

    def __initContributors(self):
        self.cardContributors.setTitle(self.tr("Contributors"))
        self.listContributors = ListContributors(self)
        self.cardContributors.viewLayout.addWidget(self.listContributors)

    def __initProjectList(self):
        self.cardProjectList.setTitle(self.tr("Project List"))

    def __initMore(self):
        self.cardMore.setTitle(self.tr("More"))


class viewStartup(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.resize(800, 600)
        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.view = ui_viewStartup()
        self.vBoxLayout.addWidget(self.view)
