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
# @file        widget_control_manager.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-16     xqyjlj       initial version
#

from enum import Enum

from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget

from common import SIGNAL_BUS
from .widget_control_io_manager import WidgetControlIoManager
from .widget_control_ip_manager import WidgetControlIpManager


class StackedWidgetIndex(Enum):
    WIDGET_CONTROL_IO_MANAGER = 0
    WIDGET_CONTROL_IP_MANAGER = 1


class WidgetControlManager(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        # ----------------------------------------------------------------------
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self)
        self.widget_widgetControlIoManager = WidgetControlIoManager(self)
        self.stackedWidget.addWidget(self.widget_widgetControlIoManager)
        self.widget_widgetControlIpManager = WidgetControlIpManager(self)
        self.stackedWidget.addWidget(self.widget_widgetControlIpManager)
        self.verticalLayout.addWidget(self.stackedWidget)
        # ----------------------------------------------------------------------

        SIGNAL_BUS.controlManagerTriggered.connect(self.__on_x_controlManagerTriggered)

    def __on_x_controlManagerTriggered(self, module: str, widget: str):
        if widget == "widget_control_io_manager":
            self.stackedWidget.setCurrentIndex(
                int(StackedWidgetIndex.WIDGET_CONTROL_IO_MANAGER.value)
            )
            self.widget_widgetControlIoManager.setInstance(module)
        else:  # widget_control_ip_manager
            self.stackedWidget.setCurrentIndex(
                int(StackedWidgetIndex.WIDGET_CONTROL_IP_MANAGER.value)
            )
