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
# @file        signal.py
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


class Signal(Base):
    def __init__(
        self,
        root: etree.Element,
        namespace: dict[str, str],
        share: Share,
    ):
        super().__init__(root, namespace)
        self.__share = share

        self.__valid = False
        for signal in self.__share.mcu.signals:
            if signal.startswith(self.__share.name) and signal.endswith(
                f"_{self.name}"
            ):
                self.__valid = True
                break

        self.__virtual = False
        if self.name in self.__share.virtual_signals:
            self.__valid = True
            self.__virtual = True

    @property
    def name(self) -> str:
        return self._get_str_attr("Name")

    @property
    def valid(self) -> bool:
        return self.__valid

    @property
    def virtual(self) -> bool:
        return self.__virtual
