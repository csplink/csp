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

from PySide6.QtCore import QRectF, Qt, QPointF
from PySide6.QtGui import (
    QFont,
    QPainterPath,
    QPainter,
    QColor,
    QPen,
    QFontMetrics,
    QAction,
)
from PySide6.QtWidgets import (
    QGraphicsObject,
    QGraphicsItem,
    QWidget,
    QStyleOptionGraphicsItem,
)
from loguru import logger
from qfluentwidgets import isDarkTheme, CheckableMenu, Action

from common import PROJECT, SummaryType, SUMMARY, IP, SIGNAL_BUS


class GraphicsItemPin(QGraphicsObject):
    DEFAULT_COLOR = QColor(185, 196, 202)
    POWER_COLOR = QColor(255, 246, 204)
    OTHER_COLOR = QColor(187, 204, 0)
    SELECTED_COLOR = QColor(0, 204, 68)
    UNSUPPORTED_COLOR = QColor(255, 211, 0)

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

    def __init__(
        self,
        width: int,
        height: int,
        pinLength: int,
        direction: Direction,
        name: str,
        type_: Type,
        pinConfig: SummaryType.PinType,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.pinLength = pinLength
        self.ellipseDia = self.pinLength // 6
        self.direction = direction
        self.name = name
        self.pinConfig = pinConfig
        self.type_ = type_
        self.menu = None
        self.highlight = False

        self.labelKey = f"pin/{self.name}/label"
        self.functionKey = f"pin/{self.name}/function"
        self.lockedKey = f"pin/{self.name}/locked"
        self.modeKey = f"pin/{self.name}/mode"

        self.setData(GraphicsItemPin.Data.LABEL_DATA.value, self.labelKey)
        self.setData(GraphicsItemPin.Data.FUNCTION_DATA.value, self.functionKey)
        self.setData(GraphicsItemPin.Data.LOCKED_DATA.value, self.lockedKey)
        self.setData(GraphicsItemPin.Data.NAME_DATA.value, name)

        self.label: str = PROJECT.project().configs.get(self.labelKey, "")  # type: ignore
        self.function: str = PROJECT.project().configs.get(self.functionKey, "")  # type: ignore
        self.locked: bool = PROJECT.project().configs.get(self.lockedKey, False)  # type: ignore
        self.mode: str = PROJECT.project().configs.get(self.modeKey, "")  # type: ignore

        self.pinInstance = SUMMARY.projectSummary().pinInstance()

        self.font = QFont("JetBrains Mono", 14, QFont.Weight.Bold)
        self.font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.fontMetrics = QFontMetrics(self.font)

        self.__initMenu()

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

        PROJECT.project().configs.pinConfigsChanged.connect(
            self.__on_project_pinConfigChanged
        )
        SIGNAL_BUS.updatePinTriggered.connect(self.__on_x_updatePinTriggered)
        SIGNAL_BUS.highlightPinTriggered.connect(self.__on_x_highlightPinTriggered)

    def boundingRect(self) -> QRectF:
        if self.type_ == self.Type.RECTANGLE_TYPE:
            return QRectF(0, 0, self.width, self.height)
        else:  # self.Type.CIRCLE_TYPE
            return QRectF(-self.width // 2, -self.height // 2, self.width, self.height)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paintRectangle(
        self, painter: QPainter, _option: QStyleOptionGraphicsItem, _widget: QWidget
    ):
        brush = painter.brush()

        # draw background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        if self.pinConfig.type == "I/O":
            if self.locked:
                painter.setBrush(self.SELECTED_COLOR)
            elif self.function:
                painter.setBrush(self.UNSUPPORTED_COLOR)
            else:
                painter.setBrush(self.DEFAULT_COLOR)
        elif self.pinConfig.type == "power":
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

        if self.highlight:
            painter.setBrush(self.SELECTED_COLOR)
            radius = self.ellipseDia // 2
            if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
                center = QPointF(x - self.ellipseDia, self.height / 2)
            elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
                center = QPointF(self.width / 2, self.pinLength + self.ellipseDia)
            elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
                center = QPointF(self.pinLength + self.ellipseDia, self.height / 2)
            else:
                center = QPointF(
                    self.width / 2, self.height - self.pinLength - self.ellipseDia
                )
            painter.drawEllipse(center, radius, radius)

        # draw text
        if (
            self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION
            or self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION
        ):
            text = self.fontMetrics.elidedText(
                self.name, Qt.TextElideMode.ElideRight, self.pinLength - 20
            )
            painter.translate(10 + x, (self.height / 2) + 8)
        else:
            text = self.fontMetrics.elidedText(
                self.name, Qt.TextElideMode.ElideRight, self.pinLength - 20
            )
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
                diff = 20 + self.ellipseDia * 2
                if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
                    text = self.fontMetrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.width - self.pinLength - diff,
                    )
                    pixels = self.fontMetrics.horizontalAdvance(text)
                    painter.translate(-pixels - diff, 0)
                elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
                    text = self.fontMetrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.height - self.pinLength - diff,
                    )
                    pixels = self.fontMetrics.horizontalAdvance(text)
                    painter.translate(-pixels - diff, 0)
                elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
                    text = self.fontMetrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.width - self.pinLength - diff,
                    )
                    painter.translate(self.pinLength + self.ellipseDia * 2, 0)
                else:
                    text = self.fontMetrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.height - self.pinLength - diff,
                    )
                    painter.translate(self.pinLength + self.ellipseDia * 2, 0)

            if isDarkTheme():
                painter.setPen(QPen(QColor(255, 255, 255), 1))

            painter.drawText(0, 0, text)

        painter.resetTransform()
        painter.setBrush(brush)

    def paintCircle(
        self, painter: QPainter, _option: QStyleOptionGraphicsItem, _widget: QWidget
    ):
        brush = painter.brush()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawEllipse(0, 0, self.width // 2, self.width // 2)

    # noinspection PyMethodOverriding
    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        if self.type_ == self.Type.RECTANGLE_TYPE:
            self.paintRectangle(painter, option, widget)
        elif self.type_ == self.Type.CIRCLE_TYPE:
            self.paintCircle(painter, option, widget)
        else:
            super().paint(painter, option, widget)

    def menuTriggered(self, action: QAction):
        if action.isCheckable():  # function
            if action.isChecked():  # set function
                function = action.text()
                seqs = function.split(":")
                instance = seqs[0]
                if instance == self.pinInstance and function in self.pinConfig.modes:
                    PROJECT.project().configs.set(self.lockedKey, True)
                else:
                    PROJECT.project().configs.set(self.lockedKey, False)
                PROJECT.project().configs.set(self.functionKey, function)
            else:  # unset function
                PROJECT.project().configs.set(self.lockedKey, False)
                PROJECT.project().configs.set(self.functionKey, "")
        else:  # reset state
            PROJECT.project().configs.set(self.lockedKey, False)
            PROJECT.project().configs.set(self.functionKey, "")
            PROJECT.project().configs.set(self.labelKey, "")

        self.updatePin()

    def __on_project_pinConfigChanged(
        self, keys: list[str], oldValue: object, newValue: object
    ):
        if keys[1] != self.name:
            return

        if keys[-1] == "label":  # update pin label comment
            self.label = newValue  # type: ignore
        elif keys[-1] == "locked":  # update pin locked status
            self.locked = newValue  # type: ignore
        elif keys[-1] == "function":  # update pin function
            self.function = newValue  # type: ignore
        elif keys[-1] == "mode":  # update pin mode
            self.mode = newValue  # type: ignore

        self.__flushMenuAction()

        self.update()

    def __initMenu(self):
        if self.pinConfig.type == "I/O":  # only "I/O" type can init menu
            self.menu = CheckableMenu()
            self.menu.view.setStyleSheet(
                """MenuActionListWidget {
                        font: 12px "JetBrains Mono", "Segoe UI", "Microsoft YaHei", "PingFang SC";
                        font-weight: normal;
                }"""
            )
            self.menu.clear()
            self.menu.triggered.connect(self.menuTriggered)
            self.menu.addAction(Action(self.tr("Reset State")))  # type: ignore
            self.menu.addSeparator()

            for function in self.pinConfig.functions():
                action = Action(function)
                action.setCheckable(True)
                self.menu.addAction(action)

            self.setData(GraphicsItemPin.Data.MENU_DATA.value, self.menu)
            self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

            self.__flushMenuAction()

    def __flushMenuAction(self):
        if self.menu is not None:
            actions = self.menu.actions()
            for action in actions:
                if action.isCheckable():
                    if action.isChecked():
                        action.setChecked(False)
                    if action.text() == self.function:
                        action.setChecked(True)
                if self.mode:
                    action.setEnabled(False)
                else:
                    action.setEnabled(True)

    def __on_x_updatePinTriggered(self, name: str):
        if name != self.name:
            return
        self.updatePin()

    def __on_x_highlightPinTriggered(self, names: list[str]):
        if self.name in names:
            self.highlight = True
        else:
            self.highlight = False
        self.update()

    def updatePin(self):
        if self.function:  # set new function
            instance = self.function.split(":")[0]
            ip = IP.projectIps().get(self.pinInstance)

            PROJECT.project().configs.set(f"{self.pinInstance}/{self.name}", {})

            if ip is None:
                return

            if instance == self.pinInstance:
                function = self.function
            else:
                function = self.mode

            seqs = function.split(":")
            if len(seqs) != 2:
                return

            mode = seqs[1]

            if mode in ip.pinModes:
                ip_modes = ip.pinModes[mode]
            else:
                logger.error(f"invalid mode: {mode}")
                return

            for key, info in ip_modes.items():
                PROJECT.project().configs.set(
                    f"{self.pinInstance}/{self.name}/{key}", info.default
                )
        else:  # clear function
            PROJECT.project().configs.set(f"{self.pinInstance}/{self.name}", {})
