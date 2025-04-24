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
# @file        project.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#

import json
import os
from typing import Any


class Project:
    class Configs:
        def __init__(self, data: dict):
            self._data = data

        def __str__(self) -> str:
            return json.dumps(self._data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self._data

        def get(self, path: str, default=None) -> Any:
            item = self._data
            keys = path.split(".")
            for key in keys:
                if key not in item:
                    return default
                item = item[key]
            return item

    class Gen:
        class Linker:
            def __init__(self, data: dict):
                self._data = data

            def __str__(self) -> str:
                return json.dumps(self._data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self._data

            @property
            def default_heap_size(self) -> int:
                return self._data.get("defaultHeapSize", -1)

            @property
            def default_stack_size(self) -> int:
                return self._data.get("defaultStackSize", -1)

        def __init__(self, data: dict):
            self._data = data
            self._linker = self.Linker(self._data.get("linker", {}))

        def __str__(self) -> str:
            return json.dumps(self._data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self._data

        @property
        def builder(self) -> str:
            return self._data["builder"]

        @property
        def copy_library(self) -> bool:
            return self._data.get("copyLibrary", True)

        @property
        def use_toolchains_package(self) -> bool:
            return self._data.get("useToolchainsPackage", False)

        @property
        def toolchains(self) -> str:
            return self._data["toolchains"]

        @property
        def builder_version(self) -> str:
            return self._data.get("builderVersion", "")

        @property
        def toolchains_version(self) -> str:
            return self._data.get("toolchainsVersion", "")

        @property
        def hal(self) -> str:
            return self._data["hal"]

        @property
        def hal_version(self) -> str:
            return self._data.get("halVersion", "")

        @property
        def linker(self) -> Linker:
            return self._linker

    def __init__(self, data: dict, path: str):
        self._data = data
        self._gen = self.Gen(self._data.get("gen", {}))
        self._configs = self.Configs(self._data.get("configs", {}))
        self._path = path

    def __str__(self) -> str:
        return json.dumps(self._data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self._data

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def target_chip(self) -> str:
        return self._data["targetChip"]

    @property
    def vendor(self) -> str:
        return self._data["vendor"]

    @property
    def version(self) -> str:
        return self._data["version"]

    @property
    def modules(self) -> list[str]:
        return self._data.get("modules", [])

    @property
    def gen(self) -> Gen:
        return self._gen

    @property
    def configs(self) -> Configs:
        return self._configs

    def hal_folder(self) -> str:
        return "C:/Users/xqyjl/Documents/git/github/csplink/csp_hal_apm32f1" # TODO

    def toolchains_folder(self) -> str:
        return "C:/Users/xqyjl/Documents/git/github/csplink/csp_hal_apm32f1" # TODO

    def path(self) -> str:
        return self._path

    def folder(self) -> str:
        return os.path.dirname(self._path)
