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
        pin_length: int,
        direction: Direction,
        name: str,
        type_: Type,
        pin_config: SummaryType.PinType,
    ):
        super().__init__()

        self.width = width
        self.height = height
        self.pin_length = pin_length
        self.ellipse_dia = self.pin_length // 6
        self.direction = direction
        self.name = name
        self.pin_config = pin_config
        self.type_ = type_
        self.menu = None
        self.highlight = False

        self.label_key = f"pin/{self.name}/label"
        self.function_key = f"pin/{self.name}/function"
        self.locked_key = f"pin/{self.name}/locked"
        self.mode_key = f"pin/{self.name}/mode"

        self.setData(GraphicsItemPin.Data.LABEL_DATA.value, self.label_key)
        self.setData(GraphicsItemPin.Data.FUNCTION_DATA.value, self.function_key)
        self.setData(GraphicsItemPin.Data.LOCKED_DATA.value, self.locked_key)
        self.setData(GraphicsItemPin.Data.NAME_DATA.value, name)

        self.label: str = PROJECT.project().configs.get(self.label_key, "")  # type: ignore
        self.function: str = PROJECT.project().configs.get(self.function_key, "")  # type: ignore
        self.locked: bool = PROJECT.project().configs.get(self.locked_key, False)  # type: ignore
        self.mode: str = PROJECT.project().configs.get(self.mode_key, "")  # type: ignore

        self.pin_instance = SUMMARY.project_summary().pin_instance()

        self.font = QFont("JetBrains Mono", 14, QFont.Weight.Bold)
        self.font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
        self.font_metrics = QFontMetrics(self.font)

        self.__init_menu()

        self.setAcceptHoverEvents(True)
        self.setAcceptedMouseButtons(Qt.MouseButton.RightButton)

        PROJECT.project().configs.pin_configs_changed.connect(
            self.__on_project_pinConfigChanged
        )
        SIGNAL_BUS.update_pin_triggered.connect(self.__on_x_update_pin_triggered)
        SIGNAL_BUS.highlight_pin_triggered.connect(self.__on_x_highlight_pin_triggered)

    # region overrides

    def boundingRect(self) -> QRectF:
        if self.type_ == self.Type.RECTANGLE_TYPE:
            return QRectF(0, 0, self.width, self.height)
        else:  # self.Type.CIRCLE_TYPE
            return QRectF(-self.width // 2, -self.height // 2, self.width, self.height)

    def shape(self) -> QPainterPath:
        path = QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        if self.type_ == self.Type.RECTANGLE_TYPE:
            self.paint_rectangle(painter, option, widget)
        elif self.type_ == self.Type.CIRCLE_TYPE:
            self.paint_circle(painter, option, widget)
        else:
            super().paint(painter, option, widget)

    # endregion

    def paint_rectangle(
        self, painter: QPainter, _option: QStyleOptionGraphicsItem, _widget: QWidget
    ):
        brush = painter.brush()

        # draw background
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        if self.pin_config.type == "I/O":
            if self.locked:
                painter.setBrush(self.SELECTED_COLOR)
            elif self.function:
                painter.setBrush(self.UNSUPPORTED_COLOR)
            else:
                painter.setBrush(self.DEFAULT_COLOR)
        elif self.pin_config.type == "power":
            painter.setBrush(self.POWER_COLOR)
        else:
            painter.setBrush(self.OTHER_COLOR)

        # draw body
        if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
            x = self.width - 100
            y = 0
            width = self.pin_length
            height = self.height
        elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
            x = 0
            y = 0
            width = self.width
            height = self.pin_length
        elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
            x = 0
            y = 0
            width = self.pin_length
            height = self.height
        else:
            x = 0
            y = self.height - self.pin_length
            width = self.width
            height = self.pin_length

        painter.drawRect(x, y, width, height)

        if self.highlight:
            painter.setBrush(self.SELECTED_COLOR)
            radius = self.ellipse_dia // 2
            if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
                center = QPointF(x - self.ellipse_dia, self.height / 2)
            elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
                center = QPointF(self.width / 2, self.pin_length + self.ellipse_dia)
            elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
                center = QPointF(self.pin_length + self.ellipse_dia, self.height / 2)
            else:
                center = QPointF(
                    self.width / 2, self.height - self.pin_length - self.ellipse_dia
                )
            painter.drawEllipse(center, radius, radius)

        # draw text
        if (
            self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION
            or self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION
        ):
            text = self.font_metrics.elidedText(
                self.name, Qt.TextElideMode.ElideRight, self.pin_length - 20
            )
            painter.translate(10 + x, (self.height / 2) + 8)
        else:
            text = self.font_metrics.elidedText(
                self.name, Qt.TextElideMode.ElideRight, self.pin_length - 20
            )
            painter.translate((self.width / 2) + 8, self.pin_length - 10 + y)
            painter.rotate(-90)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.setFont(self.font)
        painter.drawText(0, 0, text)

        # draw label
        if self.pin_config.type == "I/O":
            if self.label == "":
                text = self.function
            else:
                if self.function == "":
                    text = self.label
                else:
                    text = f"{self.label}({self.function})"

            if text != "":
                diff = 20 + self.ellipse_dia * 2
                if self.direction == GraphicsItemPin.Direction.LEFT_DIRECTION:
                    text = self.font_metrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.width - self.pin_length - diff,
                    )
                    pixels = self.font_metrics.horizontalAdvance(text)
                    painter.translate(-pixels - diff, 0)
                elif self.direction == GraphicsItemPin.Direction.BOTTOM_DIRECTION:
                    text = self.font_metrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.height - self.pin_length - diff,
                    )
                    pixels = self.font_metrics.horizontalAdvance(text)
                    painter.translate(-pixels - diff, 0)
                elif self.direction == GraphicsItemPin.Direction.RIGHT_DIRECTION:
                    text = self.font_metrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.width - self.pin_length - diff,
                    )
                    painter.translate(self.pin_length + self.ellipse_dia * 2, 0)
                else:
                    text = self.font_metrics.elidedText(
                        text,
                        Qt.TextElideMode.ElideRight,
                        self.height - self.pin_length - diff,
                    )
                    painter.translate(self.pin_length + self.ellipse_dia * 2, 0)

            if isDarkTheme():
                painter.setPen(QPen(QColor(255, 255, 255), 1))

            painter.drawText(0, 0, text)

        painter.resetTransform()
        painter.setBrush(brush)

    def paint_circle(
        self, painter: QPainter, _option: QStyleOptionGraphicsItem, _widget: QWidget
    ):
        brush = painter.brush()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(0, 0, 0), 1))
        painter.drawEllipse(0, 0, self.width // 2, self.width // 2)

    def menu_triggered(self, action: QAction):
        if action.isCheckable():  # function
            if action.isChecked():  # set function
                function = action.text()
                seqs = function.split(":")
                instance = seqs[0]
                if instance == self.pin_instance and function in self.pin_config.modes:
                    PROJECT.project().configs.set(self.locked_key, True)
                else:
                    PROJECT.project().configs.set(self.locked_key, False)
                PROJECT.project().configs.set(self.function_key, function)
            else:  # unset function
                PROJECT.project().configs.set(self.locked_key, False)
                PROJECT.project().configs.set(self.function_key, "")
        else:  # reset state
            PROJECT.project().configs.set(self.locked_key, False)
            PROJECT.project().configs.set(self.function_key, "")
            PROJECT.project().configs.set(self.label_key, "")

        self.update_pin()

    def __on_project_pinConfigChanged(
        self, keys: list[str], old_value: object, new_value: object
    ):
        if keys[1] != self.name:
            return

        if keys[-1] == "label":  # update pin label comment
            self.label = new_value  # type: ignore
        elif keys[-1] == "locked":  # update pin locked status
            self.locked = new_value  # type: ignore
        elif keys[-1] == "function":  # update pin function
            self.function = new_value  # type: ignore
        elif keys[-1] == "mode":  # update pin mode
            self.mode = new_value  # type: ignore

        self.__flush_menu_action()

        self.update()

    def __init_menu(self):
        if self.pin_config.type == "I/O":  # only "I/O" type can init menu
            self.menu = CheckableMenu()
            self.menu.view.setStyleSheet(
                """MenuActionListWidget {
                        font: 12px "JetBrains Mono", "Segoe UI", "Microsoft YaHei", "PingFang SC";
                        font-weight: normal;
                }"""
            )
            self.menu.clear()
            self.menu.triggered.connect(self.menu_triggered)
            self.menu.addAction(Action(self.tr("Reset State")))  # type: ignore
            self.menu.addSeparator()

            for function in self.pin_config.functions():
                action = Action(function)
                action.setCheckable(True)
                self.menu.addAction(action)

            self.setData(GraphicsItemPin.Data.MENU_DATA.value, self.menu)
            self.setFlags(QGraphicsItem.GraphicsItemFlag.ItemIsFocusable)

            self.__flush_menu_action()

    def __flush_menu_action(self):
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

    def __on_x_update_pin_triggered(self, name: str):
        if name != self.name:
            return
        self.update_pin()

    def __on_x_highlight_pin_triggered(self, names: list[str]):
        if self.name in names:
            self.highlight = True
        else:
            self.highlight = False
        self.update()

    def update_pin(self):
        if self.function:  # set new function
            instance = self.function.split(":")[0]
            ip = IP.project_ips().get(self.pin_instance)

            PROJECT.project().configs.set(f"{self.pin_instance}/{self.name}", {})

            if ip is None:
                return

            if instance == self.pin_instance:
                function = self.function
            else:
                function = self.mode

            seqs = function.split(":")
            if len(seqs) != 2:
                return

            mode = seqs[1]

            if mode in ip.pin_modes:
                ip_modes = ip.pin_modes[mode]
            else:
                logger.error(f"invalid mode: {mode}")
                return

            for key, info in ip_modes.items():
                PROJECT.project().configs.set(
                    f"{self.pin_instance}/{self.name}/{key}", info.default
                )
        else:  # clear function
            PROJECT.project().configs.set(f"{self.pin_instance}/{self.name}", {})
