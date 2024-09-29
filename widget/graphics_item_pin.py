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
# @file        graphics_item_pin.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-27     xqyjlj       initial version
#

from enum import Enum

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QFont, QPainterPath, QPainter, QColor, QPen, QFontMetrics, QAction
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem, QWidget, QStyleOptionGraphicsItem
from qfluentwidgets import (isDarkTheme, CheckableMenu, Action)

from common import PROJECT, SIGNAL_BUS


class GraphicsItemPin(QGraphicsObject):
    PIN_LENGTH = 100
    DEFAULT_COLOR = QColor(185, 196, 202)
    POWER_COLOR = QColor(255, 246, 204)
    OTHER_COLOR = QColor(187, 204, 0)
    SELECTED_COLOR = QColor(0, 204, 68)

    name = ""
    locked = False
    label = ""
    signal = ""
    currentCheckedAction = None
    previousCheckedAction = None

    class Direction(Enum):
        TOP = 0
        BOTTOM = 1
        LEFT = 2
        RIGHT = 3

    class Data(Enum):
        MENU_KEY = 0
        LABEL_KEY = 1
        FUNCTION_KEY = 2
        LOCKED_KEY = 3
        NAME = 4

    def __init__(self, width: int, height: int, direction: Direction, name: str, pinConfig: dict):
        super().__init__()

        self.width = int(width)
        self.height = int(height)
        self.direction = direction
        self.name = name
        self.pinConfig = pinConfig

        self.labelKey = f"pin/{self.name}/label"
        self.signalKey = f"pin/{self.name}/signal"
        self.lockedKey = f"pin/{self.name}/locked"

        self.setData(GraphicsItemPin.Data.LABEL_KEY.value, self.labelKey)
        self.setData(GraphicsItemPin.Data.FUNCTION_KEY.value, self.signalKey)
        self.setData(GraphicsItemPin.Data.LOCKED_KEY.value, self.lockedKey)
        self.setData(GraphicsItemPin.Data.NAME.value, name)

        self.label = PROJECT.config(self.labelKey, "")
        self.signal = PROJECT.config(self.signalKey, "")
        self.locked = PROJECT.config(self.lockedKey, False)

        self.font = QFont("JetBrains Mono", 14, QFont.Weight.Bold)
        self.font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.fontMetrics = QFontMetrics(self.font)

        if self.pinConfig["type"] == "I/O":
            self.menu = CheckableMenu()
            self.menu.view.setStyleSheet('''MenuActionListWidget {
                        font: 12px "JetBrains Mono", "Segoe UI", "Microsoft YaHei", "PingFang SC";
                        font-weight: normal;
                }''')
            self.menu.clear()
            self.menu.triggered.connect(self.menuTriggered)
            self.menu.addAction(Action(self.tr("Reset State")))
            self.menu.addSeparator()
            if "signals" in pinConfig:
                for name, signal in pinConfig["signals"].items():
                    action = Action(name)
                    action.setCheckable(True)
                    if self.signal == name:
                        action.setChecked(True)
                        self.currentCheckedAction = action
                        self.previousCheckedAction = action
                    self.menu.addAction(action)

            self.setData(GraphicsItemPin.Data.MENU_KEY.value, self.menu)

            self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

        PROJECT.pinConfigChanged.connect(self.__on_project_pinConfigChanged)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, self.width, self.height)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        brush = painter.brush()

        # draw background
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        if self.pinConfig["type"] == "I/O":
            if self.locked:
                painter.setBrush(self.SELECTED_COLOR)
            else:
                painter.setBrush(self.DEFAULT_COLOR)
        elif self.pinConfig["type"] == "Power":
            painter.setBrush(self.POWER_COLOR)
        else:
            painter.setBrush(self.OTHER_COLOR)

        # draw body
        if self.direction == GraphicsItemPin.Direction.LEFT:
            x = self.width - 100
            y = 0
            width = self.PIN_LENGTH
            height = self.height
        elif self.direction == GraphicsItemPin.Direction.BOTTOM:
            x = 0
            y = 0
            width = self.width
            height = self.PIN_LENGTH
        elif self.direction == GraphicsItemPin.Direction.RIGHT:
            x = 0
            y = 0
            width = self.PIN_LENGTH
            height = self.height
        else:
            x = 0
            y = self.height - self.PIN_LENGTH
            width = self.width
            height = self.PIN_LENGTH

        painter.drawRect(x, y, width, height)

        # draw text
        if self.direction == GraphicsItemPin.Direction.LEFT or self.direction == GraphicsItemPin.Direction.RIGHT:
            text = self.fontMetrics.elidedText(self.name, Qt.TextElideMode.ElideRight, self.PIN_LENGTH - 20)
            painter.translate(10 + x, (self.height / 2) + 8)
        else:
            text = self.fontMetrics.elidedText(self.name, Qt.TextElideMode.ElideRight, self.PIN_LENGTH - 20)
            painter.translate((self.width / 2) + 8, self.PIN_LENGTH - 10 + y)
            painter.rotate(-90)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setFont(self.font)
        painter.drawText(0, 0, text)

        # draw label
        if self.pinConfig["type"] == "I/O":
            if self.label == "":
                text = self.signal
            else:
                if self.signal == "":
                    text = self.label
                else:
                    text = f"{self.label}({self.signal})"

            if text != "":
                if self.direction == GraphicsItemPin.Direction.LEFT:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.width - self.PIN_LENGTH - 20)
                    pixels = self.fontMetrics.horizontalAdvance(text)
                    painter.translate(-pixels - 20, 0)
                elif self.direction == GraphicsItemPin.Direction.BOTTOM:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.height - self.PIN_LENGTH - 20)
                    pixels = self.fontMetrics.horizontalAdvance(text)
                    painter.translate(-pixels - 20, 0)
                elif self.direction == GraphicsItemPin.Direction.RIGHT:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.width - self.PIN_LENGTH - 20)
                    painter.translate(self.PIN_LENGTH, 0)
                else:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.height - self.PIN_LENGTH - 20)
                    painter.translate(self.PIN_LENGTH, 0)

            if isDarkTheme():
                painter.setPen(QPen(QColor(255, 255, 255), 1))

            painter.drawText(0, 0, text)

        painter.resetTransform()
        painter.setBrush(brush)

    def menuTriggered(self, action: QAction):
        self.currentCheckedAction = action
        if action.isCheckable():
            if self.previousCheckedAction is not None and self.previousCheckedAction != action:
                self.previousCheckedAction.setChecked(False)
            if action.isChecked():
                PROJECT.setConfig(self.lockedKey, True)
                PROJECT.setConfig(self.signalKey, action.text())
            else:
                PROJECT.setConfig(self.lockedKey, False)
                PROJECT.setConfig(self.signalKey, "")
        else:
            if self.previousCheckedAction is not None:
                self.previousCheckedAction.setChecked(False)
            self.previousCheckedAction = None
            PROJECT.setConfig(self.lockedKey, False)
            PROJECT.setConfig(self.signalKey, "")
            PROJECT.setConfig(self.labelKey, "")

        if self.previousCheckedAction != action:
            self.previousCheckedAction = action

    def __on_project_pinConfigChanged(self, keys: list[str], oldValue: str, newValue: str):
        if keys[1] == self.name:
            if keys[-1] == "label":
                self.label = newValue
                SIGNAL_BUS.gridPropertyIpTriggered.emit(PROJECT.summary.pinIp, self.name)
            elif keys[-1] == "locked":
                self.locked = newValue
            elif keys[-1] == "signal":
                self.signal = newValue
                pin = PROJECT.summary.pins[self.name]
                if newValue != "":
                    instance = newValue.split("-")[0]
                    info = pin["signals"][newValue]
                    if info is not None and "mode" in info:
                        mode = info["mode"]
                        ip = PROJECT.ip.ip(instance)
                        ip_modes = ip["modes"][mode]
                        path = f"{instance}/{self.name}"
                        PROJECT.setConfig(path, {})
                        for key, info in ip_modes.items():
                            path = f"{instance}/{self.name}/{key}"
                            PROJECT.setConfig(path, info["default"])
                    elif oldValue != "" and oldValue is not None:
                        instance = oldValue.split("-")[0]
                        info = pin["signals"][oldValue]
                        if info is not None and "mode" in info:
                            path = f"{instance}/{self.name}"
                            PROJECT.setConfig(path, {})
                    SIGNAL_BUS.gridPropertyIpTriggered.emit(instance, self.name)
                elif oldValue != "" and oldValue is not None:
                    instance = oldValue.split("-")[0]
                    info = pin["signals"][oldValue]
                    if info is not None and "mode" in info:
                        path = f"{instance}/{self.name}"
                        PROJECT.setConfig(path, {})
                    SIGNAL_BUS.gridPropertyIpTriggered.emit(instance, self.name)
            self.update()
