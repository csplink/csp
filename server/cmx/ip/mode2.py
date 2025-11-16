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
from .share import Share
from .signal_logical_op import SignalLogicalOp


class Mode2(Base):
    def __init__(self, root: etree.Element, namespace: dict[str, str], share: Share):
        super().__init__(root, namespace)
        self.__share = share

        self.__semaphores: list[str] = []
        for node in self._root.findall("ns:Semaphore", self._namespace):
            self.__semaphores.append(node.text or "")

        self.__conditions: list[Condition] = []
        for node in self._root.findall("ns:Condition", self._namespace):
            self.__conditions.append(Condition(node, namespace, share))

        self.__valid = False
        self.__signal_logical_ops: list[SignalLogicalOp] = []
        for node in self._root.findall("ns:SignalLogicalOp", self._namespace):
            logical = SignalLogicalOp(node, self._namespace, self.__share)
            self.__valid |= logical.valid
            self.__signal_logical_ops.append(logical)

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
        return name

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
    def semaphores(self) -> list[str]:
        return self.__semaphores

    @property
    def conditions(self) -> list[Condition]:
        return self.__conditions

    @property
    def signal_logical_ops(self) -> list[SignalLogicalOp]:
        return self.__signal_logical_ops

    @property
    def valid(self) -> bool:
        return self.__valid
