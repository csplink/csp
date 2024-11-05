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
import os
from pathlib import Path

import jinja2
import yaml
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QPixmap, Qt, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsPixmapItem, QGraphicsProxyWidget, QGraphicsItem
from qfluentwidgets import isDarkTheme, applyThemeColor, LineEdit

from common import Icon, SETTINGS, PROJECT, Style, SUMMARY
from tools import Drawio
from view.ui.clock_tree_view_ui import Ui_ClockTreeView


class ClockTreeView(Ui_ClockTreeView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.__multiple = 1

        self.__resPath = Path(
            SETTINGS.DATABASE_FOLDER) / 'clock' / PROJECT.vendor.lower() / SUMMARY.projectSummary().clockTree.lower()
        self.__svgPath = str(self.__resPath) + ".svg"
        self.__ymlPath = str(self.__resPath) + ".yml"

        self.__drawio = Drawio(self.__svgPath)

        self.zoomInBtn.setIcon(Icon.ZOOM_IN)
        self.zoomResetBtn.setIcon(Icon.REFRESH)
        self.zoomOutBtn.setIcon(Icon.ZOOM_OUT)

        self.__scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.__scene)

        self.zoomInBtn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.zoomResetBtn.pressed.connect(lambda: self.graphicsView.rescale())
        self.zoomOutBtn.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        self.__updateGraphicsViewBackgroundColor()
        SETTINGS.themeChanged.connect(lambda theme: self.__updateGraphicsViewBackgroundColor())

    def __getSvg(self) -> QGraphicsSvgItem | QGraphicsPixmapItem:

        renderer = QSvgRenderer(self.__drawio.svg, self)

        if SETTINGS.clockTreeType.value == "Pixmap":
            self.__multiple = 5
            pixmap = QPixmap(renderer.defaultSize() * self.__multiple)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter()
            painter.begin(pixmap)
            painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                                   QPainter.RenderHint.TextAntialiasing |
                                   QPainter.RenderHint.SmoothPixmapTransform)
            renderer.render(painter)
            painter.end()
            item = QGraphicsPixmapItem(pixmap)
            item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        else:
            self.__multiple = 1
            item = QGraphicsSvgItem()
            item.setMaximumCacheSize(renderer.defaultSize() * 2)
            item.setSharedRenderer(renderer)

        return item

    def __updateGraphicsViewBackgroundColor(self):
        self.__scene.clear()
        self.__scene.setBackgroundBrush(QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253))
        self.__scene.addItem(self.__getSvg())
        self.__addWidget()

        self.graphicsView.rescale()
        self.graphicsView.update()

    def __addWidget(self):
        widgetsGeom = self.__drawio.widgets

        with open(self.__ymlPath, 'r', encoding='utf-8') as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
        widgets = config.get('widgets', {})

        data = {
            "multiple": self.__multiple,
            "isDarkMode": isDarkTheme(),
        }

        env = jinja2.Environment(loader=jinja2.FileSystemLoader([os.path.dirname(Style.T_CLOCK_TREE_VIEW.path())]),
                                 line_comment_prefix="//")
        template = env.get_template('clock_tree_view.qss.j2')
        context = template.render(data)
        context = applyThemeColor(context)

        for id_, geom in widgetsGeom.items():
            cfg = widgets.get('widgets')

        for id_, cfg in widgets.items():
            stylesheet = context
            if cfg.get('widget') is not None:
                widget = cfg['widget']
                if widget == 'numberLineBox':
                    w = LineEdit()
                    w.setAlignment(Qt.AlignmentFlag.AlignCenter)
                else:
                    w = QWidget()
                    stylesheet = 'QWidget { background-color: rgb(255, 0, 0); }'
            else:
                w = QWidget()
                stylesheet = 'QWidget { background-color: rgb(255, 0, 0); }'

            size = QSize(int(widgetsGeom[id_]['width']), int(widgetsGeom[id_]['height'])) * self.__multiple
            w.setStyleSheet(stylesheet)
            w.setFixedSize(size)
            w.setProperty('config', cfg)
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(w)
            proxy.setCacheMode(QGraphicsItem.CacheMode.ItemCoordinateCache, size)
            proxy.setPos(widgetsGeom[id_]['x'] * self.__multiple, widgetsGeom[id_]['y'] * self.__multiple)
            self.__scene.addItem(proxy)
