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
from __future__ import annotations

import os
from pathlib import Path

import jinja2
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsProxyWidget,
    QButtonGroup,
)
from qfluentwidgets import isDarkTheme, BodyLabel

from common import Icon, SETTINGS, PROJECT, Style, SUMMARY, IP, CLOCK_TREE
from tools import Drawio
from view.ui.clock_tree_view_ui import Ui_ClockTreeView
from widget import (
    FloatClockTreeWidget,
    IntegerClockTreeWidget,
    EnumClockTreeWidget,
    RadioClockTreeWidget,
    NumberClockTreeWidget,
)


class ClockTreeView(Ui_ClockTreeView, QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.__resPath = (
            Path(SETTINGS.DATABASE_FOLDER)
            / "clock"
            / PROJECT.project().vendor.lower()
            / SUMMARY.projectSummary().clockTree.lower()
        )
        self.__svgPath = str(self.__resPath) + ".svg"
        self.__ymlPath = str(self.__resPath) + ".yml"

        self.__clockTree = CLOCK_TREE.getClockTree(
            PROJECT.project().vendor, SUMMARY.projectSummary().clockTree
        )
        self.__drawio = Drawio(
            self.__svgPath,
            self.__clockTree.i18nOrigin(),
            SETTINGS.get(SETTINGS.language).value.name(),
        )
        self.__radioGroup: dict[str, QButtonGroup] = {}

        self.zoomInBtn.setIcon(Icon.ZOOM_IN)
        self.zoomResetBtn.setIcon(Icon.REFRESH)
        self.zoomOutBtn.setIcon(Icon.ZOOM_OUT)

        self.__scene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.__scene)

        self.zoomInBtn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.zoomResetBtn.pressed.connect(lambda: self.graphicsView.rescale())
        self.zoomOutBtn.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        self.__updateGraphicsViewBackgroundColor()
        SETTINGS.themeChanged.connect(
            lambda theme: self.__updateGraphicsViewBackgroundColor()
        )

    def __getSvg(self) -> QGraphicsSvgItem | QGraphicsPixmapItem:

        renderer = QSvgRenderer(self.__drawio.svg, self)

        item = QGraphicsSvgItem()
        # item.setMaximumCacheSize(renderer.defaultSize() * 2)
        item.setSharedRenderer(renderer)

        return item

    def __updateGraphicsViewBackgroundColor(self):
        self.__scene.clear()
        self.__scene.setBackgroundBrush(
            QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253)
        )
        self.__scene.addItem(self.__getSvg())
        self.__addWidget()

        self.graphicsView.rescale()
        self.graphicsView.update()

    def __addWidget(self):
        geoms = self.__drawio.widgets

        elements = self.__clockTree.elements

        data = {
            "isDarkMode": isDarkTheme(),
        }

        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                [os.path.dirname(Style.T_CLOCK_TREE_VIEW.path())]
            ),
            line_comment_prefix="//",
        )
        template = env.get_template("clock_tree_view.qss.j2")

        widgetGroups = {}
        for id_, geom in geoms.items():
            data["width"] = geom.width
            data["height"] = geom.height
            widget = None
            z = -1
            if id_ in elements:
                element = elements.get(id_)
                if (
                    element is not None
                    and element.origin is not None
                    and len(element.origin) > 0
                ):
                    refParameter: str = element.refParameter
                    z = element.z
                    seqs = refParameter.split(":")
                    if len(seqs) == 2:
                        instance = seqs[0]
                        name = seqs[1]
                        ip = IP.projectIps().get(instance)
                        parameter = ip.parameters.get(name)
                        if parameter is not None:
                            type_ = parameter.type
                            if type_ == "float":
                                widget = FloatClockTreeWidget(
                                    id_,
                                    instance,
                                    name,
                                    element,
                                    parameter,
                                    self.__clockTree,
                                    template,
                                    data,
                                )
                            elif type_ == "integer":
                                widget = IntegerClockTreeWidget(
                                    id_,
                                    instance,
                                    name,
                                    element,
                                    parameter,
                                    self.__clockTree,
                                    template,
                                    data,
                                )
                            elif type_ == "enum":
                                widget = EnumClockTreeWidget(
                                    id_,
                                    instance,
                                    name,
                                    element,
                                    parameter,
                                    self.__clockTree,
                                    template,
                                    data,
                                )
                            elif type_ == "radio":
                                if parameter.group not in self.__radioGroup:
                                    group = QButtonGroup()
                                    self.__radioGroup[parameter.group] = group
                                else:
                                    group = self.__radioGroup[parameter.group]
                                widget = RadioClockTreeWidget(
                                    id_,
                                    instance,
                                    name,
                                    element,
                                    parameter,
                                    self.__clockTree,
                                    template,
                                    data,
                                )
                                group.addButton(widget)
                            if widget is not None:
                                widgetGroups[id_] = widget
            if widget is None:  # default use body label, and font is red
                # noinspection PyTypeChecker
                widget = BodyLabel(id_)
                widget.setProperty("unused", True)
                stylesheet = f'BodyLabel {{font: 12px "Segoe UI", "Microsoft YaHei"; color: red;}}'
                widget.setStyleSheet(stylesheet)
            size = QSize(int(geom.width), int(geom.height))
            widget.setFixedSize(size)
            # w.setProperty('config', element)
            proxy = QGraphicsProxyWidget()
            proxy.setWidget(widget)
            proxy.setPos(geom.x, geom.y)
            if z >= 0:
                proxy.setZValue(z)
            elif isinstance(widget, EnumClockTreeWidget):
                proxy.setZValue(1)
            self.__scene.addItem(proxy)

        for id_, widget in widgetGroups.items():  # init connect
            widget.binding(widgetGroups)

        for id_, widget in widgetGroups.items():
            if not (
                isinstance(widget, NumberClockTreeWidget)
                and not widget.parameter.readonly
            ):
                widget.setup()

        for id_, widget in widgetGroups.items():
            if (
                isinstance(widget, NumberClockTreeWidget)
                and not widget.parameter.readonly
            ):
                widget.setup()
