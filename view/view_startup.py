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

from .ui.ui_view_startup import Ui_view_startup

from common import Database
from widget import list_contributors


class ui_view_startup(Ui_view_startup, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__init_card_command()
        self.__init_contributors()
        self.__init_project_list()
        self.__init_more()

    def __init_card_command(self):
        self.card_command.setTitle(self.tr("Command"))
        self.btn_new_chip_project = PushButton(self.tr("New Chip Project"))
        self.btn_open_project = PushButton(self.tr("Open Project"))
        self.card_command.viewLayout.setContentsMargins(30, 30, 30, 30)
        self.card_command.viewLayout.setDirection(QBoxLayout.Direction.TopToBottom)
        self.card_command.viewLayout.addWidget(self.btn_new_chip_project)
        self.card_command.viewLayout.addWidget(self.btn_open_project)

    def __init_contributors(self):
        self.card_contributors.setTitle(self.tr("Contributors"))
        self.m_list_contributors = list_contributors(self)
        self.card_contributors.viewLayout.addWidget(self.m_list_contributors)

    def __init_project_list(self):
        self.card_project_list.setTitle(self.tr("Project List"))

    def __init_more(self):
        self.card_more.setTitle(self.tr("More"))


class view_startup(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.view = ui_view_startup()
        self.vBoxLayout.addWidget(self.view)
