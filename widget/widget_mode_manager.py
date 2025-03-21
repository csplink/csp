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

        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(9, 9, 9, 9)
        self.tab_view = TabWidget(self)
        self.v_layout.addWidget(self.tab_view)

        self.mode_manager = ModeManager(self)
        self.mode_manager.setObjectName("ModeManager")
        self.pin_map_manager = PinMapManager(self)
        self.pin_map_manager.setObjectName("PinMapManager")

        self.tab_view.add_sub_interface(self.mode_manager, "Mode", True)
        self.tab_view.add_sub_interface(self.pin_map_manager, "Pin Map", True)

    def set_target(self, instance: str, target: str):
        self.mode_manager.set_target(instance, target)
