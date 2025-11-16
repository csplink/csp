#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        ref_mode.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import copy
import xml.etree.ElementTree as etree

from blinker import Signal as BlinkSignal
from utils.express import Express

from .base import Base
from .condition import Condition
from .parameter import Parameter
from .share import Share


class RefMode(Base):
    def __init__(self, root: etree.Element, namespace: dict[str, str], share: Share):
        super().__init__(root, namespace)
        self.__share = share
        self.__base_mode_obj = None

        self.__emitter = {
            "update": BlinkSignal("update"),
        }

        self.__parameters: dict[str, Parameter] = self.build_origin_parameters()

        self.__always_false = False
        self.__always_true = True
        self.__conditions: list[Condition] = []
        expressions = []
        condition_nodes = self._root.findall("ns:Condition", self._namespace)
        for node in condition_nodes:
            condition = Condition(node, namespace, share)
            if condition.status == Express.Status.ALWAYS_TRUE:
                expressions.append("(true)")
            elif condition.status == Express.Status.ALWAYS_FALSE:
                expressions.append("(false)")
                self.__always_false = True
                self.__always_true = False
            else:
                expressions.append(f"({condition.expression})")
                self.__always_true = False
            self.__conditions.append(condition)
        self.__expressions = " and ".join(expressions)

    @property
    def emitter(self):
        return self.__emitter

    @property
    def name(self) -> str:
        return self._get_str_attr("Name")

    @property
    def hal_mode(self) -> str:
        return self._get_str_attr("HalMode")

    @property
    def base_mode(self) -> str:
        return self._get_str_attr("BaseMode")

    @property
    def base_mode_obj(self) -> RefMode | None:
        return self.__base_mode_obj

    @property
    def config_for_mode(self) -> str:
        return self._root.findtext("ns:ConfigForMode", "", self._namespace)

    @property
    def parameters(self) -> dict[str, Parameter]:
        return self.__parameters

    @property
    def conditions(self) -> list[Condition]:
        return self.__conditions

    @property
    def expressions(self) -> str:
        return self.__expressions

    @property
    def always_false(self) -> bool:
        return self.__always_false

    @property
    def always_true(self) -> bool:
        return self.__always_true

    @property
    def id(self) -> str:
        conditions = []
        for condition in self.conditions:
            conditions.append(f"{condition.expression}")
        if not conditions:
            conditions = ["default"]
        return f"{self.name}@({' && '.join(conditions)!r})"

    def build_origin_parameters(self) -> dict[str, Parameter]:
        parameters = {}
        for node in self._root.findall("ns:Parameter", self._namespace):
            name = node.attrib.get("Name", "")
            parameters[name] = Parameter(node, self._namespace)
        return parameters

    def set_base_mode_obj(self, obj: RefMode):
        obj.emitter["update"].connect(self.on_base_mode_obj_update)
        self.__base_mode_obj = obj
        parameters = copy.deepcopy(obj.parameters)
        parameters.update(self.__parameters)
        self.__parameters = parameters

        self.__emitter["update"].send(obj.name)

    def on_base_mode_obj_update(self, sender, **kwargs):
        print("update from", self.name, sender)
        pass
