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
# @file        number_clock_tree_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-05     xqyjlj       initial version
#

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QLineEdit
from jinja2 import Template
from loguru import logger
from qfluentwidgets import applyThemeColor

from common import ClockTreeType, IpType, PROJECT, SETTINGS
from utils import Express
from .base_clock_tree_widget import BaseClockTreeWidget


class NumberClockTreeWidget(BaseClockTreeWidget, QLineEdit):
    def __init__(
        self,
        id_: str,
        instance: str,
        param: str,
        element: ClockTreeType.ElementUnitType,
        parameter: IpType.ParameterUnitType,
        clock_tree: ClockTreeType,
        template: Template,
        data: dict,
        parent=None,
    ):
        BaseClockTreeWidget.__init__(
            self, id_, instance, param, element, parameter, clock_tree, template, data
        )
        QLineEdit.__init__(self, parent)

        self.valid = True

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setReadOnly(parameter.readonly)
        self.setStyleSheet(self.stylesheet)

        self.data["valid"] = False
        context = template.render(self.data)
        self.invalid_stylesheet = applyThemeColor(context)

        self.editingFinished.connect(self.__on_editingFinished)

    def __range_tool_tip(self) -> str:
        if self.parameter.max > -1 and self.parameter.min > -1:
            max_ = self.__display_value(self.parameter.max)
            min_ = self.__display_value(self.parameter.min)
            return f"({min_} ~ {max_})"
        else:
            return ""

    def value(self) -> float:
        super().value()
        if len(self.inputs()) == 1:
            value = self.inputs()[self.element.input[0]].value()
            # sometimes it needs to initialize itself
            if self.__real_value(self.text() or "0") != value:
                self.__set_value(value)
        else:
            value = self.__real_value(self.text() or "0")
        return value

    def setup(self):
        super().setup()
        num = PROJECT.project().configs.get(
            f"{self.instance}/{self.param}"
        )  # first used project data
        if num is None:
            if len(self.inputs()) == 1:
                num = self.inputs()[self.element.input[0]].value()  # used input data
            else:
                num = self.parameter.default  # used default data
        self.__set_value(num)  # type: ignore
        self.setReadOnly(self.parameter.readonly)

        local = SETTINGS.get(SETTINGS.language).value.name()
        self.setToolTip(
            f"{self.parameter.description.get(local)} {self.__range_tool_tip()}"
        )

    def flush(self, source: BaseClockTreeWidget):
        self.__set_value(source.value())
        super().flush(source)

    def __display_value(self, value: float) -> str:
        expression = self.parameter.expression.display
        if len(expression) == 0:
            result = str(value)
        else:
            result = str(Express.float_expr(expression, {"value": value}))
        return self.__strip(result)

    def __real_value(self, value: float | str) -> float:
        result = float(value)
        expression = self.parameter.expression.real
        if len(expression) > 0:
            result = Express.float_expr(expression, {"value": result})
        return result

    def __strip(self, value: str) -> str:
        return value.rstrip("0").rstrip(".")

    def __set_value(self, value: float):
        text = self.__display_value(value)
        if text != self.text():
            self.setText(text)
            self.__value_updated(value)

    def __value_updated(self, value: float):
        PROJECT.project().configs.set(f"{self.instance}/{self.param}", value)
        for id_, widget in self.outputs().items():
            widget.flush(self)

        if (
            self.parameter.max >= value >= self.parameter.min
            or self.parameter.max == -1
        ):
            if not self.valid:
                self.setStyleSheet(self.stylesheet)
            self.valid = True
        else:
            if self.valid:
                self.setStyleSheet(self.invalid_stylesheet)
            self.valid = False
            logger.warning(
                f"invalid number in widget:{self.id} with ‘{self.__display_value(value)}', range '{self.__range_tool_tip()}'."
            )

    def __on_editingFinished(self):
        text = self.text()
        if len(text) > 0:
            self.__value_updated(self.__real_value(text))
        else:
            logger.warning(f"invalid number in widget:{self.id} with 'null'")
