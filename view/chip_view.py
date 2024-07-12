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
from enum import Enum

from PyQt5.QtCore import QItemSelection
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QMessageBox

from qfluentwidgets import (isDarkTheme)

from .ui.Ui_chip_view import Ui_ChipView
from common import Style, Icon, PROJECT, SETTINGS
from widget import LQFP


class StackedWidgetIndex(Enum):
    MODE_GRID_IO = 0


class ChipView(Ui_ChipView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.toolButton_zoomIn.setIcon(Icon.ZOOM_IN)
        self.toolButton_zoomReset.setIcon(Icon.REFRESH)
        self.toolButton_zoomOut.setIcon(Icon.ZOOM_OUT)

        self.splitter.setSizes([500, 100])
        self.splitter_2.setSizes([500, 200])
        self.splitter_3.setSizes([200, 1000])

        self.toolButton_zoomIn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.toolButton_zoomReset.pressed.connect(lambda: self.graphicsView.resize())
        self.toolButton_zoomOut.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        self.treeView_modules.header().hide()
        locale = SETTINGS.get(SETTINGS.language).value
        model = QStandardItemModel(self.treeView_modules)
        for group, module_group in PROJECT.modules.items():
            item = QStandardItem(group)
            item.setEditable(False)
            model.appendRow(item)
            for name, module in module_group.items():
                item_child = QStandardItem(name)
                item_child.setEditable(False)
                item_child.setToolTip(module["description"][locale.name()])
                item.appendRow(item_child)
        self.treeView_modules.setModel(model)
        self.treeView_modules.expandAll()
        self.treeView_modules.selectionModel().selectionChanged.connect(self.treeView_modulesSelectionChanged)

        scene = QGraphicsScene(self.graphicsView)
        scene.setBackgroundBrush(QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253))

        if PROJECT.package != "unknown":
            if re.match("^LQFP\d+$", PROJECT.package):
                items = LQFP().getItems(PROJECT.vendor, PROJECT.targetChip)
            else:
                QMessageBox.critical(self, self.tr("critical"),
                                     self.tr(f"The package '{PROJECT.package}' is not supported at this time"))
            if items != None:
                for item in items:
                    scene.addItem(item)
        self.graphicsView.setScene(scene)
        self.graphicsView.resize()

        Style.CHIP_VIEW.apply(self)

    def treeView_modulesSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            if str(index.parent().data()) != "None":
                module = str(index.data())
                ip = PROJECT.ip(module)
                if "modeGrid" in ip and ip["modeGrid"] == "mode_grid_io":
                    self.stackedWidget.setCurrentIndex(int(StackedWidgetIndex.MODE_GRID_IO.value))
                    self.widget_modeGridIo.setInstance(module)
