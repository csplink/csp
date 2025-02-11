#!/usr/bin/env python3
# -*- coding:utf-8 -*-\

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
# @file        stacked_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-06     xqyjlj       initial version
#

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QStackedWidget, QWidget


class StackedWidget(QFrame):
    currentChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = QStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

    def addWidget(self, widget: QWidget):
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    # noinspection PyUnusedLocal
    def setCurrentWidget(self, widget: QWidget, popOut: bool = True):
        self.view.setCurrentWidget(widget)

    # noinspection PyUnusedLocal
    def setCurrentIndex(self, index: int, popOut: bool = True):
        self.view.setCurrentIndex(index)

    def currentIndex(self) -> int:
        return self.view.currentIndex()

    def currentWidget(self) -> QWidget:
        return self.view.currentWidget()

    def indexOf(self, widget) -> int:
        return self.view.indexOf(widget)

    def count(self) -> int:
        return self.view.count()
