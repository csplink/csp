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
# @file        base_clock_tree_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-05     xqyjlj       initial version
#
from __future__ import annotations

import copy

from jinja2 import Template
from loguru import logger
from qfluentwidgets import applyThemeColor

from common import IpType, ClockTreeType, IP


class BaseClockTreeWidget:
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
    ):
        self.id = id_
        self.instance = instance
        self.param = param
        self.element = element
        self.parameter = parameter
        self.clock_tree = clock_tree
        self.ip = IP.project_ips()[self.instance]
        self.template = template
        self.data = copy.deepcopy(data)
        self.data["valid"] = True

        self.__inputs = {}
        self.__outputs = {}
        self.__is_setup = False

        context = template.render(self.data)
        self.stylesheet = applyThemeColor(context)

        self.ip.parameter_item_updated.connect(self.__on_ip_parameterItemUpdated)

    def __repr__(self):
        module = self.__class__.__module__
        classname = self.__class__.__name__
        address = hex(id(self))

        # noinspection PyUnresolvedReferences
        return f"<{module}.{classname}({address}, id={self.id!r}, name={self.objectName()!r}, value={self.value()!r}) at {address}>"  # type: ignore

    def value(self) -> float:
        if not self.__is_setup:
            self.setup()
        return -1

    def inputs(self) -> dict[str, BaseClockTreeWidget]:
        return self.__inputs

    def outputs(self) -> dict[str, BaseClockTreeWidget]:
        return self.__outputs

    def binding(self, group: dict[str, BaseClockTreeWidget]):
        for id_ in self.element.input:
            if id_ not in group:
                logger.error(f'The input id "{id_}" is not defined')
            else:
                self.__inputs[id_] = group[id_]
        for id_ in self.element.output:
            if id_ not in group:
                logger.error(f'The input id "{id_}" is not defined')
            else:
                self.__outputs[id_] = group[id_]

    def setup(self):
        self.__is_setup = True

    def flush(self, source: BaseClockTreeWidget):
        for id_, widget in self.outputs().items():
            widget.flush(self)

    def __on_ip_parameterItemUpdated(self, names: list[str]):
        if self.param in names:
            self.parameter = self.ip.parameters[self.param]
            self.setup()
