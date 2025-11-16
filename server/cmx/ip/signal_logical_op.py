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
# @file        signal_logical_op.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree

from .base import Base
from .share import Share
from .signal import Signal


class SignalLogicalOp(Base):
    def __init__(self, root: etree.Element, namespace: dict[str, str], share: Share):
        super().__init__(root, namespace)
        self.__share = share

        self.__valid = False

        self.__signals: dict[str, Signal] = {}
        self.__virtual = True
        for node in self._root.findall("ns:Signal", self._namespace):
            signal = Signal(node, self._namespace, self.__share)
            self.__valid |= signal.valid
            self.__signals[signal.name] = signal
            self.__virtual &= signal.virtual

    @property
    def name(self) -> str:
        return self._get_str_attr("Name")

    @property
    def signals(self) -> dict[str, Signal]:
        return self.__signals

    @property
    def valid(self) -> bool:
        return self.__valid

    @property
    def virtual(self) -> bool:
        return self.__virtual
