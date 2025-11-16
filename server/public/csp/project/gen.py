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
# @file        gen.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#


import json

from .linker import Linker


class Gen:

    def __init__(self, data: dict):
        self._data = data
        self._linker = Linker(self._data.get("linker", {}))

    def __str__(self) -> str:
        return json.dumps(self._data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self._data

    @property
    def builder(self) -> str:
        return self._data["builder"]

    @property
    def copyLibrary(self) -> bool:
        return self._data.get("copyLibrary", True)

    @property
    def useToolchainsPackage(self) -> bool:
        return self._data.get("useToolchainsPackage", False)

    @property
    def toolchains(self) -> str:
        return self._data["toolchains"]

    @property
    def builderVersion(self) -> str:
        return self._data.get("builderVersion", "")

    @property
    def toolchainsVersion(self) -> str:
        return self._data.get("toolchainsVersion", "")

    @property
    def hal(self) -> str:
        return self._data["hal"]

    @property
    def halVersion(self) -> str:
        return self._data.get("halVersion", "")

    @property
    def linker(self) -> Linker:
        return self._linker
