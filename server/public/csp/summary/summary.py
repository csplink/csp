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
# @file        summary.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#

from __future__ import annotations

import json

from ..i18n import I18n
from .document import Documents
from .linker import Linker
from .module import Modules
from .pin import Pin


class Summary:

    def __init__(self, data: dict):
        self.__data = data

        self.__vendorUrl = None
        self.__documents = None
        self.__illustrate = None
        self.__introduction = None
        self.__modules = None
        self.__url = None
        self.__linker = None
        self.__pins = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @property
    def clockTree(self) -> str:
        return self.__data.get("clockTree", "")

    @property
    def core(self) -> str:
        return self.__data.get("core", "")

    @property
    def io(self) -> int:
        return self.__data.get("io", 0)

    @property
    def die(self) -> str:
        return self.__data.get("die", "")

    @property
    def frequency(self) -> int:
        return self.__data.get("frequency", 0)

    @property
    def series(self) -> str:
        return self.__data.get("series", "")

    @property
    def line(self) -> str:
        return self.__data.get("line", "")

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @property
    def vendorUrl(self) -> I18n:
        if self.__vendorUrl is None:
            self.__vendorUrl = I18n(self.__data.get("vendorUrl", {}))
        return self.__vendorUrl

    @property
    def documents(self) -> Documents:
        if self.__documents is None:
            self.__documents = Documents(self.__data.get("documents", {}))
        return self.__documents

    @property
    def hals(self) -> list[str]:
        return self.__data.get("hals", [])

    @property
    def hasPowerPad(self) -> bool:
        return self.__data.get("hasPowerPad", False)

    @property
    def illustrate(self) -> I18n:
        if self.__illustrate is None:
            self.__illustrate = I18n(self.__data.get("illustrate", {}))
        return self.__illustrate

    @property
    def introduction(self) -> I18n:
        if self.__introduction is None:
            self.__introduction = I18n(self.__data.get("introduction", {}))
        return self.__introduction

    @property
    def modules(self) -> Modules:
        if self.__modules is None:
            self.__modules = Modules(self.__data.get("modules", {}))
        return self.__modules

    @property
    def package(self) -> str:
        return self.__data.get("package", "")

    @property
    def url(self) -> I18n:
        if self.__url is None:
            self.__url = I18n(self.__data.get("url", {}))
        return self.__url

    @property
    def builders(self) -> dict[str, dict[str, list[str]]]:
        return self.__data.get("builders", {})

    @property
    def linker(self) -> Linker:
        if self.__linker is None:
            self.__linker = Linker(self.__data.get("linker", {}))
        return self.__linker

    @property
    def pins(self) -> dict[str, Pin]:
        if self.__pins is None:
            self.__pins = {}
            pins = self.__data.get("pins", {})
            for name, unit in pins.items():
                self.__pins[name] = Pin(unit if unit is not None else {})
        return self.__pins
