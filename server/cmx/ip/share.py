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
# @file        share.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import re

from utils.express import Express

from ..mcu import CmxMcu


class Share:
    def __init__(self, name: str, alias: str, mcu: CmxMcu, virtual_signals: list[str]):
        self._name = name
        self._alias = alias
        self._mcu = mcu
        self._label = alias or name
        self._virtual_signals = virtual_signals

    @property
    def name(self) -> str:
        return self._name

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def mcu(self) -> CmxMcu:
        return self._mcu

    @property
    def label(self) -> str:
        return self.name or self.name

    @property
    def virtual_signals(self) -> list[str]:
        return self._virtual_signals

    def beautify_text(self, html: str) -> str:
        text = re.sub(r"<br\s*/?>", "\n", html, flags=re.IGNORECASE)
        text = Express.replace_word_keep_case(text, self.name, self.label)
        return text
