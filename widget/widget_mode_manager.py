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
# @file        widget_mode_manager.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-01     xqyjlj       initial version
#


from PySide6.QtWidgets import QWidget, QVBoxLayout
from loguru import logger

from .widget_base_manager import WidgetBaseManager, WidgetBaseManagerType
from .tab_widget import TabWidget


class ModeManager(WidgetBaseManager):

    def __init__(self, parent=None):
        super().__init__(WidgetBaseManagerType.MODE, parent)


class PinMapManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class WidgetModeManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(9, 9, 9, 9)
        self.tabView = TabWidget(self)
        self.vLayout.addWidget(self.tabView)

        self.modeManager = ModeManager(self)
        self.modeManager.setObjectName("ModeManager")
        self.pinMapManager = PinMapManager(self)
        self.pinMapManager.setObjectName("PinMapManager")

        self.tabView.addSubInterface(self.modeManager, "Mode", True)
        self.tabView.addSubInterface(self.pinMapManager, "Pin Map", True)

    def setTarget(self, instance: str, target: str):
        self.modeManager.setTarget(instance, target)
