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
# @file        soc_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import re

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QGraphicsScene, QMessageBox
from qfluentwidgets import (isDarkTheme)

from common import Style, Icon, PROJECT, SETTINGS
from widget import LQFP
from .ui.soc_view_ui import Ui_SocView


class SocView(Ui_SocView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.zoomInBtn.setIcon(Icon.ZOOM_IN)
        self.zoomResetBtn.setIcon(Icon.REFRESH)
        self.zoomOutBtn.setIcon(Icon.ZOOM_OUT)

        self.modulePropertySocSplitter.setSizes([100, 300, 300])
        self.modulePropertySocSplitter.setCollapsible(0, False)
        self.modulePropertySocSplitter.setCollapsible(1, False)
        self.modePropertySplitter.setSizes([300, 100])
        self.modePropertySplitter.setCollapsible(0, False)
        self.modePropertySplitter.setCollapsible(1, False)

        self.zoomInBtn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.zoomResetBtn.pressed.connect(lambda: self.graphicsView.rescale())
        self.zoomOutBtn.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        self.__scene = QGraphicsScene(self.graphicsView)
        self.__updateGraphicsViewBackgroundColor()

        SETTINGS.themeChanged.connect(lambda theme: self.__updateGraphicsViewBackgroundColor())

        if PROJECT.summary.package != "":
            if re.match("^LQFP\d+$", PROJECT.summary.package):
                items = LQFP().getItems(PROJECT.vendor, PROJECT.targetChip)
            else:
                items = None
                QMessageBox.critical(self, self.tr('critical'),
                                     self.tr(f'The package "{PROJECT.summary.package}" is not supported at this time'))
            if items is not None:
                for item in items:
                    self.__scene.addItem(item)
        self.graphicsView.setScene(self.__scene)
        self.graphicsView.rescale()

        Style.SOC_VIEW.apply(self)

    def __updateGraphicsViewBackgroundColor(self):
        self.__scene.setBackgroundBrush(QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253))
