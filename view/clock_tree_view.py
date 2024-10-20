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
# @file        clock_tree_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-19     xqyjlj       initial version
#

import xml.etree.ElementTree as etree
from pathlib import Path

from PySide6.QtGui import QColor, QPainter, QPixmap, Qt
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem
from qfluentwidgets import isDarkTheme

from common import Icon, SETTINGS, PROJECT
from view.ui.clock_tree_view_ui import Ui_ClockTreeView


class ClockTreeView(Ui_ClockTreeView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.zoomInBtn.setIcon(Icon.ZOOM_IN)
        self.zoomResetBtn.setIcon(Icon.REFRESH)
        self.zoomOutBtn.setIcon(Icon.ZOOM_OUT)

        self.__scene = QGraphicsScene(self.graphicsView)
        self.__scene.addItem(self.__getSvg())

        self.graphicsView.setScene(self.__scene)
        self.graphicsView.rescale()

        self.zoomInBtn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.zoomResetBtn.pressed.connect(lambda: self.graphicsView.rescale())
        self.zoomOutBtn.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        self.__updateGraphicsViewBackgroundColor()
        SETTINGS.themeChanged.connect(lambda theme: self.__updateGraphicsViewBackgroundColor())

    def __getSvg(self) -> QGraphicsPixmapItem:
        svgPath = Path(
            SETTINGS.DATABASE_FOLDER) / 'clock' / PROJECT.vendor.lower() / f'{PROJECT.summary.clockTree.lower()}.svg'
        with open(svgPath, 'r', encoding='utf-8') as f:
            svg = f.read()

        root = etree.fromstring(svg)
        print(root.attrib['content'])

        if isDarkTheme():  # TODO: 修改时钟树主题样式
            svg = svg.replace('rgb(0, 0, 0)', 'rgb(0, 159, 170)')
            svg = svg.replace('fill="#000000"', 'fill="#FDFDFD"')

        renderer = QSvgRenderer(svg.encode('utf-8'))
        pixmap = QPixmap(renderer.defaultSize() * 5)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter()
        painter.begin(pixmap)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        renderer.render(painter)
        painter.end()
        pixmapItem = QGraphicsPixmapItem(pixmap)
        pixmapItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)

        return pixmapItem

    def __updateGraphicsViewBackgroundColor(self):
        self.__scene.clear()
        self.__scene.setBackgroundBrush(QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253))
        self.__scene.addItem(self.__getSvg())
        self.graphicsView.rescale()
