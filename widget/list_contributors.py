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
# @file        list_contributors.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-02     xqyjlj       initial version
#

import os

from PySide6.QtCore import Qt, Signal, QItemSelection, QObject, QEvent
from PySide6.QtGui import QShowEvent, QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout

from qfluentwidgets import (PixmapLabel, FlowLayout, ScrollArea)

from .ui.ui_list_contributors import Ui_list_contributors

from common import Database, CONTRIBUTORS_FILE


class list_contributors(Ui_list_contributors, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.flow_widget = QWidget(self)
        self.flow_layout = FlowLayout(self.flow_widget, needAni=True)
        self.flow_layout.setContentsMargins(0, 0, 0, 0)
        self.flow_layout.setVerticalSpacing(20)
        self.flow_layout.setHorizontalSpacing(10)
        self.scroll_area.setWidget(self.flow_widget)
        self.scroll_area.enableTransparentBackground()

        contributors = Database.get_contributors()

        for contributor in contributors:
            label = PixmapLabel()
            label.installEventFilter(self)
            label.setFixedSize(40, 40)
            label.setPixmap(
                QPixmap(f'{os.path.dirname(CONTRIBUTORS_FILE)}/{contributor["avatar"]}').scaled(
                    40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.flow_layout.addWidget(label)

    def eventFilter(self, watched: QObject, event: QEvent):
        if isinstance(watched, PixmapLabel):
            if event.type() == QEvent.Type.MouseButtonRelease:
                print(111)

        return super().eventFilter(watched, event)
