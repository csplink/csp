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
# @file        enum_clock_tree_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-05     xqyjlj       initial version
#

from PySide6.QtGui import Qt, QMouseEvent, QKeyEvent, QWheelEvent
from PySide6.QtWidgets import QComboBox, QStyleFactory, QListWidget, QListWidgetItem
from jinja2 import Template

from common import ClockTreeType, IpType, PROJECT, IP, SETTINGS
from utils import Express
from .base_clock_tree_widget import BaseClockTreeWidget


class EnumClockTreeWidget(BaseClockTreeWidget, QComboBox):
    def __init__(
        self,
        id_: str,
        instance: str,
        param: str,
        element: ClockTreeType.ElementUnitType,
        parameter: IpType.ParameterUnitType,
        clockTree: ClockTreeType,
        template: Template,
        data: dict,
        parent=None,
    ):
        BaseClockTreeWidget.__init__(
            self, id_, instance, param, element, parameter, clockTree, template, data
        )
        QComboBox.__init__(self, parent)

        self.setObjectName("enumWidget")
        self.setStyle(
            QStyleFactory.create("windows")
        )  # Removing this will cause qss rendering exception
        self.setStyleSheet(self.stylesheet)

        self.__listWidget = QListWidget(self)
        self.__listWidget.setObjectName("listWidget")
        self.__listWidget.setStyleSheet(self.stylesheet)

        self.setView(self.__listWidget)

        self.readonly = parameter.readonly

        self.currentTextChanged.connect(self.__on_currentTextChanged)

    def mousePressEvent(self, event: QMouseEvent):
        if not self.readonly:
            super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if not self.readonly:
            super().keyPressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        if not self.readonly:
            super().wheelEvent(event)

    def value(self) -> float:
        super().value()
        value = self.parameter.values.get(IP.iptr2(self.param, self.currentText()))
        if value is None:
            return 0
        expression = value.expression.real
        if len(expression) > 0:
            if len(self.inputs()) == 1:
                num = Express.floatExpr(
                    expression, {"value": self.inputs()[self.element.input[0]].value()}
                )
                return num
        return 0

    def setup(self):
        super().setup()
        self.currentTextChanged.disconnect(self.__on_currentTextChanged)

        self.__listWidget.clear()

        for key, value in self.parameter.values.items():
            item = QListWidgetItem(IP.iptr(self.param, key))
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.__listWidget.addItem(item)
        self.setModel(self.__listWidget.model())

        val = PROJECT.project().configs.get(f"{self.instance}/{self.param}")
        if val is None:
            val = self.parameter.default
        else:
            if val not in self.parameter.values:
                # logger.warning(f"The enum item {val!r} is not supported. Use default value {self.parameter.default!r}")
                val = self.parameter.default

        self.currentTextChanged.connect(self.__on_currentTextChanged)
        text = self.currentText()
        v = IP.iptr(self.param, val)
        self.setCurrentText(IP.iptr(self.param, val))
        if v == text:
            self.__on_currentTextChanged(text)

        local = SETTINGS.get(SETTINGS.language).value.name()
        self.setToolTip(self.parameter.description.get(local))

    def flush(self, source: BaseClockTreeWidget):
        super().flush(source)

    def __on_currentTextChanged(self, text: str):
        PROJECT.project().configs.set(
            f"{self.instance}/{self.param}", IP.iptr2(self.param, text)
        )
        for id_, widget in self.outputs().items():
            widget.flush(self)
