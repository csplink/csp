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
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QFrame, QLabel, QHBoxLayout, QFrame, QSizePolicy

from qframelesswindow import (FramelessWindow, StandardTitleBar)

from .ui.ui_view_startup import Ui_view_startup


class ui_view_startup(Ui_view_startup, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class view_startup(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.vBoxLayout = QHBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.view = ui_view_startup()
        self.vBoxLayout.addWidget(self.view)
