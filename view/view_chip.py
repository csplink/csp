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
# @file        view_chip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import re

from PySide6.QtCore import QItemSelection
from PySide6.QtGui import QColor, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMessageBox

from qfluentwidgets import (isDarkTheme)

from .ui.ui_view_chip import Ui_view_chip
from common import Style, Icon, PROJECT, SETTINGS
from widget import LQFP


class view_chip(Ui_view_chip, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.btn_zoom_in.setIcon(Icon.ZOOM_IN)
        self.btn_zoom_reset.setIcon(Icon.REFRESH)
        self.btn_zoom_out.setIcon(Icon.ZOOM_OUT)

        self.splitter_1.setSizes([100, 300])
        self.splitter_1.setCollapsible(0, False)
        self.splitter_1.setCollapsible(1, False)
        self.splitter_2.setSizes([300, 100])
        self.splitter_2.setCollapsible(0, False)
        self.splitter_2.setCollapsible(1, False)

        self.btn_zoom_in.pressed.connect(lambda: self.graphics_view.zoomIn(6))
        self.btn_zoom_reset.pressed.connect(lambda: self.graphics_view.resize())
        self.btn_zoom_out.pressed.connect(lambda: self.graphics_view.zoomOut(6))

        scene = QGraphicsScene(self.graphics_view)
        scene.setBackgroundBrush(QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253))

        if PROJECT.summary.package != "unknown":
            if re.match("^LQFP\d+$", PROJECT.summary.package):
                items = LQFP().getItems(PROJECT.vendor, PROJECT.target_chip)
            else:
                QMessageBox.critical(self, self.tr("critical"),
                                     self.tr(f"The package '{PROJECT.summary.package}' is not supported at this time"))
            if items != None:
                for item in items:
                    scene.addItem(item)
        self.graphics_view.setScene(scene)
        self.graphics_view.resize()

        Style.VIEW_CHIP.apply(self)
