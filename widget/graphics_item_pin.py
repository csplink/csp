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
from loguru import logger
from qfluentwidgets import (isDarkTheme, CheckableMenu, Action)

from common import PROJECT, SIGNAL_BUS, SummaryType, SUMMARY, IP


class GraphicsItemPin(QGraphicsObject):
    DEFAULT_COLOR = QColor(185, 196, 202)
    POWER_COLOR = QColor(255, 246, 204)
    OTHER_COLOR = QColor(187, 204, 0)
    SELECTED_COLOR = QColor(0, 204, 68)

    class Direction(Enum):
        TOP_DIRECTION = 0
        BOTTOM_DIRECTION = 1
        LEFT_DIRECTION = 2
        RIGHT_DIRECTION = 3

    class Data(Enum):
        MENU_DATA = 0
        LABEL_DATA = 1
        FUNCTION_DATA = 2
        LOCKED_DATA = 3
        NAME_DATA = 4

    class Type(Enum):
        RECTANGLE_TYPE = 0
        CIRCLE_TYPE = 1

    def __init__(self, width: int, height: int, pinLength: int, direction: Direction, name: str, kind: Type,
                 pinConfig: SummaryType.PinType):
        super().__init__()

        self.width = int(width)
        self.height = int(height)
        self.pinLength = int(pinLength)
        self.direction = direction
        self.name = name
        self.pinConfig = pinConfig
        self.type = kind

        self.currentCheckedAction = None
        self.previousCheckedAction = None

        self.labelKey = f"pin/{self.name}/label"
        self.functionKey = f"pin/{self.name}/function"
        self.lockedKey = f"pin/{self.name}/locked"

        self.setData(GraphicsItemPin.Data.LABEL_DATA.value, self.labelKey)
        self.setData(GraphicsItemPin.Data.FUNCTION_DATA.value, self.functionKey)
        self.setData(GraphicsItemPin.Data.LOCKED_DATA.value, self.lockedKey)
        self.setData(GraphicsItemPin.Data.NAME_DATA.value, name)

        self.label = PROJECT.project().configs.get(self.labelKey, "")
        self.function = PROJECT.project().configs.get(self.functionKey, "")
        self.locked = PROJECT.project().configs.get(self.lockedKey, False)

        self.pinIp = SUMMARY.projectSummary().pinIp()

        self.font = QFont("JetBrains Mono", 14, QFont.Weight.Bold)
        self.font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.fontMetrics = QFontMetrics(self.font)

        if self.pinConfig.type == "I/O":
            self.menu = CheckableMenu()
            self.menu.view.setStyleSheet('''MenuActionListWidget {
                        font: 12px "JetBrains Mono", "Segoe UI", "Microsoft YaHei", "PingFang SC";
                        font-weight: normal;
                }''')
            self.menu.clear()
            self.menu.triggered.connect(self.menuTriggered)
            self.menu.addAction(Action(self.tr("Reset State")))
            self.menu.addSeparator()

            for function in pinConfig.functions():
                # noinspection PyTypeChecker
                action = Action(function)
                action.setCheckable(True)
                if self.function == function:
                    action.setChecked(True)
                    self.currentCheckedAction = action
                    self.previousCheckedAction = action
                self.menu.addAction(action)

            self.setData(GraphicsItemPin.Data.MENU_DATA.value, self.menu)
            self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)
        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

        PROJECT.project().configs.pinConfigsChanged.connect(self.__on_project_pinConfigChanged)

    def boundingRect(self) -> QRectF:
        if self.type == self.Type.RECTANGLE_TYPE:
            return QRectF(0, 0, self.width, self.height)
        elif self.type == self.Type.CIRCLE_TYPE:
            return QRectF(-self.width // 2, -self.height // 2, self.width, self.height)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paintRectangle(self, painter: QPainter, _option: QStyleOptionGraphicsItem, _widget: QWidget):
        brush = painter.brush()

        # draw background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        if self.pinConfig.type == "I/O":
            if self.locked:
                painter.setBrush(self.SELECTED_COLOR)
            else:
                painter.setBrush(self.DEFAULT_COLOR)
        elif self.pinConfig.type == "Power":
            painter.setBrush(self.POWER_COLOR)
        else:
            painter.setBrush(self.OTHER_COLOR)

        # draw body
        if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
            x = self.width - 100
            y = 0
            width = self.pinLength
            height = self.height
        elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
            x = 0
            y = 0
            width = self.width
            height = self.pinLength
        elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
            x = 0
            y = 0
            width = self.pinLength
            height = self.height
        else:
            x = 0
            y = self.height - self.pinLength
            width = self.width
            height = self.pinLength

        painter.drawRect(x, y, width, height)

        # draw text
        if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION or self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
            text = self.fontMetrics.elidedText(self.name, Qt.TextElideMode.ElideRight, self.pinLength - 20)
            painter.translate(10 + x, (self.height / 2) + 8)
        else:
            text = self.fontMetrics.elidedText(self.name, Qt.TextElideMode.ElideRight, self.pinLength - 20)
            painter.translate((self.width / 2) + 8, self.pinLength - 10 + y)
            painter.rotate(-90)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setFont(self.font)
        painter.drawText(0, 0, text)

        # draw label
        if self.pinConfig.type == "I/O":
            if self.label == "":
                text = self.function
            else:
                if self.function == "":
                    text = self.label
                else:
                    text = f"{self.label}({self.function})"

            if text != "":
                if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.width - self.pinLength - 20)
                    pixels = self.fontMetrics.horizontalAdvance(text)
                    painter.translate(-pixels - 20, 0)
                elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.height - self.pinLength - 20)
                    pixels = self.fontMetrics.horizontalAdvance(text)
                    painter.translate(-pixels - 20, 0)
                elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.width - self.pinLength - 20)
                    painter.translate(self.pinLength, 0)
                else:
                    text = self.fontMetrics.elidedText(text, Qt.TextElideMode.ElideRight,
                                                       self.height - self.pinLength - 20)
                    painter.translate(self.pinLength, 0)

            if isDarkTheme():
                painter.setPen(QPen(QColor(255, 255, 255), 1))

            painter.drawText(0, 0, text)

        painter.resetTransform()
        painter.setBrush(brush)

    def paintCircle(self, painter: QPainter, _option: QStyleOptionGraphicsItem, _widget: QWidget):
        brush = painter.brush()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawEllipse(0, 0, self.width // 2, self.width // 2)

    # noinspection PyMethodOverriding
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget):
        if self.type == self.Type.RECTANGLE_TYPE:
            self.paintRectangle(painter, option, widget)
        elif self.type == self.Type.CIRCLE_TYPE:
            self.paintCircle(painter, option, widget)
        else:
            super().paint(painter, option, widget)

    def menuTriggered(self, action: QAction):
        self.currentCheckedAction = action
        if action.isCheckable():
            if self.previousCheckedAction is not None and self.previousCheckedAction != action:
                self.previousCheckedAction.setChecked(False)
            if action.isChecked():
                PROJECT.project().configs.set(self.lockedKey, True)
                PROJECT.project().configs.set(self.functionKey, action.text())
            else:
                PROJECT.project().configs.set(self.lockedKey, False)
                PROJECT.project().configs.set(self.functionKey, "")
        else:
            if self.previousCheckedAction is not None:
                self.previousCheckedAction.setChecked(False)
            self.previousCheckedAction = None
            PROJECT.project().configs.set(self.lockedKey, False)
            PROJECT.project().configs.set(self.functionKey, "")
            PROJECT.project().configs.set(self.labelKey, "")

        if self.previousCheckedAction != action:
            self.previousCheckedAction = action

    def __on_project_pinConfigChanged(self, keys: list[str], oldValue: str, newValue: str):
        pin = SUMMARY.projectSummary().pins[self.name]

        # only matches own pins
        if keys[1] != self.name:
            return

        if keys[-1] == "label":  # update pin label comment
            self.label = newValue
            SIGNAL_BUS.gridPropertyIpTriggered.emit(self.pinIp, self.name)
        elif keys[-1] == "locked":  # update pin locked status
            self.locked = newValue
            SIGNAL_BUS.gridPropertyIpTriggered.emit(self.pinIp, self.name)
        elif keys[-1] == "function":  # update pin function
            self.function = newValue
            if len(newValue) > 0:  # set new function
                seqs = newValue.split("-")
                instance = seqs[0]
                mode = seqs[1]

                ip = IP.projectIps().get(instance)
                if ip is None:
                    logger.error(f'the ip instance:"{instance}" is invalid.')
                    SIGNAL_BUS.gridPropertyIpTriggered.emit(instance, self.name)
                    return
                ip_modes = ip.modes[mode]
                PROJECT.project().configs.set(f"{instance}/{self.name}", {})
                for key, info in ip_modes.items():
                    PROJECT.project().configs.set(f"{instance}/{self.name}/{key}", info.default)
                SIGNAL_BUS.gridPropertyIpTriggered.emit(instance, self.name)
            elif len(oldValue) > 0:  # newValue = None, so clear old function
                instance = oldValue.split("-")[0]
                ip = IP.projectIps().get(instance)
                if ip is None:
                    logger.error(f'the ip instance:"{instance}" is invalid.')
                    return
                PROJECT.project().configs.set(f"{instance}/{self.name}", {})
                SIGNAL_BUS.gridPropertyIpTriggered.emit(instance, self.name)

        self.update()
