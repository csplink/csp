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
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        tab_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-03-08     xqyjlj       initial version
#

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import getFont, Pivot

from .stacked_widget import StackedWidget


class TabWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tabBar = Pivot(self)
        self.stackedWidget = StackedWidget(self)

        self.vBoxLayout = QVBoxLayout(self)

        self.vBoxLayout.addWidget(self.tabBar, 0, Qt.AlignmentFlag.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

    def addSubInterface(self, view: QWidget, text, isTransparent=False):
        if not view.objectName():
            raise ValueError("The object name of `interface` can't be empty string.")
        view.setProperty("isStackedTransparent", isTransparent)
        self.stackedWidget.addWidget(view)

        routeKey = view.objectName()
        item = self.tabBar.addItem(
            routeKey=routeKey,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(view),
        )
        item.setFont(getFont(13))  # type: ignore

        if self.stackedWidget.count() == 1:
            self.stackedWidget.currentChanged.connect(
                self.__on_stackedWidget_currentChanged
            )
            self.tabBar.setCurrentItem(routeKey)

        self.__updateStackedBackground()

    def __on_stackedWidget_currentChanged(self, index: int):
        widget = self.stackedWidget.widget(index)
        self.tabBar.setCurrentItem(widget.objectName())

        self.__updateStackedBackground()

    def __updateStackedBackground(self):
        isTransparent = self.stackedWidget.currentWidget().property(
            "isStackedTransparent"
        )
        if bool(self.stackedWidget.property("isTransparent")) == isTransparent:
            return

        self.stackedWidget.setProperty("isTransparent", isTransparent)
        self.stackedWidget.setStyle(QApplication.style())
