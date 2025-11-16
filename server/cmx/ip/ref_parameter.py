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
# @file        ref_parameter.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree

from .base import Base
from .condition import Condition
from .possible_value import PossibleValue
from .share import Share


class RefParameter(Base):
    def __init__(self, root: etree.Element, namespace: dict[str, str], share: Share):
        super().__init__(root, namespace)
        self.__share = share

        self.__possible_values: dict[str, PossibleValue] = {}
        for node in self._root.findall("ns:PossibleValue", self._namespace):
            value = node.attrib.get("Value", "")
            self.__possible_values[value] = PossibleValue(node, namespace)

        expressions = []
        self.__conditions: list[Condition] = []
        for node in self._root.findall("ns:Condition", self._namespace):
            condition = Condition(node, namespace, share)
            self.__conditions.append(condition)
            expressions.append(condition.expression)
        self.__expression = " and ".join(expressions or ["default"])

    @property
    def name(self) -> str:
        return self._get_str_attr("Name")

    @property
    def type(self) -> str:
        return self._get_str_attr("Type")

    @property
    def default_value(self) -> str:
        return self._get_str_attr("DefaultValue")

    @property
    def visible(self) -> bool:
        return self._get_bool_attr("Visible", True)

    @property
    def comment(self) -> str:
        return self.__share.beautify_text(self._get_str_attr("Comment"))

    @property
    def description(self) -> str:
        text = self._root.findtext("ns:Description", "", self._namespace)
        return self.__share.beautify_text(text)

    @property
    def max(self) -> float | str | None:
        max = self._root.attrib.get("Max")
        if max is None:
            return None
        elif max.startswith("="):
            return max
        else:
            return float(self._root.attrib["Max"])

    @property
    def min(self) -> float | str | None:
        min = self._root.attrib.get("Min")
        if min is None:
            return None
        elif min.startswith("="):
            return min  # TODO
        else:
            return float(self._root.attrib["Min"])

    @property
    def group(self) -> str:
        return self._get_str_attr("Group")

    @property
    def possible_values(self) -> dict[str, PossibleValue]:
        return self.__possible_values

    @property
    def conditions(self) -> list[Condition]:
        return self.__conditions

    @property
    def expression(self) -> str:
        return self.__expression

    @property
    def id(self) -> str:
        conditions = []
        for condition in self.conditions:
            conditions.append(f"{condition.expression}")
        if not conditions:
            conditions = ["default"]
        return f"{self.name}@({' && '.join(conditions)!r})"

    def default_value_index(self) -> int:
        """返回默认值在 possible_value 列表中的索引，如果没找到返回 0"""
        default = self.default_value
        if not default:
            return 0

        for i, key in enumerate(self.possible_values):
            if key == default:
                return i
        return 0
