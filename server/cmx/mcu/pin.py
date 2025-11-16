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
# @file        pin.py
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
from .signal import Signal


class Pin(Base):
    def __init__(self, root: etree.Element, namespace: dict[str, str]):
        super().__init__(root, namespace)

        self.__signals: dict[str, Signal] = {}
        for node in self._root.findall("ns:Signal", self._namespace):
            name = node.attrib.get("Name", "")
            signal = Signal(node, namespace)
            self.__signals[name] = signal

        self.__conditions: list[Condition] = []
        for node in self._root.findall("ns:Condition", self._namespace):
            self.__conditions.append(Condition(node, namespace))

    @property
    def name(self) -> str:
        return self._get_str_attr("Name")

    @property
    def position(self) -> str:
        return self._get_str_attr("Position")

    @property
    def type(self) -> str:
        return self._get_str_attr("Type")

    @property
    def signals(self) -> dict[str, Signal]:
        return self.__signals

    @property
    def conditions(self) -> list[Condition]:
        return self.__conditions
