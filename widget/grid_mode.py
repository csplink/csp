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
# @file        grid_mode.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-16     xqyjlj       initial version
#

from enum import Enum

from PySide6.QtWidgets import QWidget

from common import SIGNAL_BUS
from .ui.grid_mode_ui import Ui_GridMode


class StackedWidgetIndex(Enum):
    GRID_MODE_IO = 0


class GridMode(Ui_GridMode, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        SIGNAL_BUS.gridModeTriggered.connect(self.changeModuleWidget)

    def changeModuleWidget(self, module: str, widget: str):
        if widget == "grid_mode_io":
            self.stackedWidget.setCurrentIndex(int(StackedWidgetIndex.GRID_MODE_IO.value))
            self.widget_gridModeIo.setInstance(module)
