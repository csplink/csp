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

        self.tab_bar = Pivot(self)
        self.stacked_widget = StackedWidget(self)

        self.v_box_layout = QVBoxLayout(self)

        self.v_box_layout.addWidget(self.tab_bar, 0, Qt.AlignmentFlag.AlignLeft)
        self.v_box_layout.addWidget(self.stacked_widget)
        self.v_box_layout.setContentsMargins(0, 0, 0, 0)

    def add_sub_interface(self, view: QWidget, text, is_transparent=False):
        if not view.objectName():
            raise ValueError("The object name of `interface` can't be empty string.")
        view.setProperty("isStackedTransparent", is_transparent)
        self.stacked_widget.addWidget(view)

        routeKey = view.objectName()
        item = self.tab_bar.addItem(
            routeKey=routeKey,
            text=text,
            onClick=lambda: self.stacked_widget.setCurrentWidget(view),
        )
        item.setFont(getFont(13))  # type: ignore

        if self.stacked_widget.count() == 1:
            self.stacked_widget.current_changed.connect(
                self.__on_stackedWidget_currentChanged
            )
            self.tab_bar.setCurrentItem(routeKey)

        self.__update_stacked_background()

    def __on_stackedWidget_currentChanged(self, index: int):
        widget = self.stacked_widget.widget(index)
        self.tab_bar.setCurrentItem(widget.objectName())

        self.__update_stacked_background()

    def __update_stacked_background(self):
        is_transparent = self.stacked_widget.currentWidget().property(
            "isStackedTransparent"
        )
        if bool(self.stacked_widget.property("isTransparent")) == is_transparent:
            return

        self.stacked_widget.setProperty("isTransparent", is_transparent)
        self.stacked_widget.setStyle(QApplication.style())
