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
# @file        chip_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import re

# from PySide6.QtCore import QItemSelection
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMessageBox

from qfluentwidgets import (isDarkTheme)

from .ui.ui_chip_view import Ui_ChipView
from common import Style, Icon, PROJECT
from widget import LQFP


class ChipView(Ui_ChipView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.zoomInBtn.setIcon(Icon.ZOOM_IN)
        self.zoomResetBtn.setIcon(Icon.REFRESH)
        self.zoomOutBtn.setIcon(Icon.ZOOM_OUT)

        # self.splitter_1.setSizes([100, 300])
        # self.splitter_1.setCollapsible(0, False)
        # self.splitter_1.setCollapsible(1, False)
        self.splitter_2.setSizes([300, 100])
        self.splitter_2.setCollapsible(0, False)
        self.splitter_2.setCollapsible(1, False)

        self.zoomInBtn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.zoomResetBtn.pressed.connect(lambda: self.graphicsView.rescale())
        self.zoomOutBtn.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        scene = QGraphicsScene(self.graphicsView)
        scene.setBackgroundBrush(QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253))

        if PROJECT.summary.package != "unknown":
            if re.match("^LQFP\d+$", PROJECT.summary.package):
                items = LQFP().getItems(PROJECT.vendor, PROJECT.targetChip)
            else:
                QMessageBox.critical(self, self.tr("critical"),
                                     self.tr(f"The package '{PROJECT.summary.package}' is not supported at this time"))
            if items != None:
                for item in items:
                    scene.addItem(item)
        self.graphicsView.setScene(scene)
        self.graphicsView.rescale()

        Style.VIEW_CHIP.apply(self)
