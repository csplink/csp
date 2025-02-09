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
# @file        radio_clock_tree_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-05     xqyjlj       initial version
#

from PySide6.QtWidgets import QRadioButton
from jinja2 import Template

from common import ClockTreeType, IpType, PROJECT, SETTINGS
from .base_clock_tree_widget import BaseClockTreeWidget


class RadioClockTreeWidget(BaseClockTreeWidget, QRadioButton):
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
        QRadioButton.__init__(self, parent)

        self.setObjectName("radioWidget")
        self.setStyleSheet(self.stylesheet)

        self.toggled.connect(self.__on_toggled)

    def value(self) -> float:
        super().value()
        if self.isChecked():
            if len(self.inputs()) == 1:
                return self.inputs()[self.element.input[0]].value()
        return 0

    def setup(self):
        super().setup()
        selector = PROJECT.project().configs.get(
            f"{self.instance}/{self.parameter.group}"
        )
        if selector is None:
            default = self.parameter.default
            if default is not None and default == True:
                self.setChecked(True)
        else:
            if selector == self.param:
                self.setChecked(True)

        local = SETTINGS.get(SETTINGS.language).value.name()
        self.setToolTip(self.parameter.description.get(local))

    def flush(self, source: BaseClockTreeWidget):
        if self.isChecked():
            super().flush(source)

    def __on_toggled(self, checked: bool):
        if checked:
            PROJECT.project().configs.set(
                f"{self.instance}/{self.parameter.group}", self.param
            )
            for id_, widget in self.outputs().items():
                widget.flush(self)
