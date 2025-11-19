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
# @file        mode1.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree

from utils.express import Express

from .base import Base
from .condition import Condition
from .mode_logic_operator2 import ModeLogicOperator2
from .share import Share


class Mode1(Base):
    def __init__(self, root: etree.Element, namespace: dict[str, str], share: Share):
        super().__init__(root, namespace)
        self.__share = share

        self.__mode_logic_operator: list[ModeLogicOperator2] = []
        for node in self._root.findall("ns:ModeLogicOperator", self._namespace):
            self.__mode_logic_operator.append(
                ModeLogicOperator2(node, self._namespace, share)
            )

        self.__semaphores: list[str] = []
        for node in self._root.findall("ns:Semaphore", self._namespace):
            self.__semaphores.append(node.text or "")

        expressions = []
        self.__conditions: list[Condition] = []
        for node in self._root.findall("ns:Condition", self._namespace):
            condition = Condition(node, namespace, share)
            self.__conditions.append(condition)
            expressions.append(condition.expression)
        self.__expression = " and ".join(expressions or ["true"])

        self.__type = "enum"
        if len(self.__mode_logic_operator) == 1:
            if len(self.__mode_logic_operator[0].modes) == 1:
                mode = next(iter(self.__mode_logic_operator[0].modes.values()))
                if not mode.remove_disable and mode.valid:
                    if len(mode.signal_logical_ops) == 0:
                        self.__type = "boolean"
                    else:
                        is_all_virtual = True
                        for op in mode.signal_logical_ops:
                            if not op.virtual:
                                is_all_virtual = False
                                break
                        if is_all_virtual:
                            self.__type = "boolean"

        self.__should_remove = False
        if self.remove_condition:
            status = Express.get_expression_status(
                self.remove_condition, self.__share.mcu.context
            )
            if status == Express.Status.ALWAYS_TRUE:
                self.__should_remove = True

    @property
    def name(self) -> str:
        name = self._get_str_attr("Name")
        return f"Ctrl_{name}"

    @property
    def user_name(self) -> str:
        return self._get_str_attr("UserName")

    @property
    def label(self) -> str:
        return self.user_name or self._get_str_attr("Name")

    @property
    def remove_condition(self) -> str:
        return self._get_str_attr("RemoveCondition")

    @property
    def remove_disable(self) -> bool:
        return self._get_bool_attr("RemoveDisable")

    @property
    def should_remove(self) -> bool:
        return self.__should_remove

    @property
    def mode_logic_operator(self) -> list[ModeLogicOperator2]:
        return self.__mode_logic_operator

    @property
    def semaphores(self) -> list[str]:
        return self.__semaphores

    @property
    def conditions(self) -> list[Condition]:
        return self.__conditions

    @property
    def expression(self) -> str:
        return self.__expression

    @property
    def type(self) -> str:
        return self.__type
