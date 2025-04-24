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
# 2025-07-09     xqyjlj       initial version
#

import json


from .i18n import I18n


class Summary:
    class Documents:
        class DocumentUnit:
            def __init__(self, data: dict):
                self.__data = data
                self.__url = None

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def url(self) -> I18n:
                if self.__url is None:
                    self.__url = I18n(self.__data.get("url", {}))
                return self.__url

        def __init__(self, data: dict):
            self.__data = data
            self.__datasheets = None
            self.__errata = None
            self.__references = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def datasheets(self) -> dict[str, DocumentUnit]:
            if self.__datasheets is None:
                self.__datasheets = {}
                datasheets = self.__data.get("datasheets", {})
                for name, unit in datasheets.items():
                    self.__datasheets[name] = Summary.Documents.DocumentUnit(
                        unit if unit is not None else {}
                    )
            return self.__datasheets

        @property
        def errata(self) -> dict[str, DocumentUnit]:
            if self.__errata is None:
                self.__errata = {}
                errata = self.__data.get("errata", {})
                for name, unit in errata.items():
                    self.__errata[name] = Summary.Documents.DocumentUnit(
                        unit if unit is not None else {}
                    )
            return self.__errata

        @property
        def references(self) -> dict[str, DocumentUnit]:
            if self.__references is None:
                self.__references = {}
                references = self.__data.get("references", {})
                for name, unit in references.items():
                    self.__references[name] = Summary.Documents.DocumentUnit(
                        unit if unit is not None else {}
                    )
            return self.__references

    class Modules:
        class ModuleUnit:
            def __init__(self, data: dict):
                self.__data = data

                self.__description = None

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def description(self) -> I18n:
                if self.__description is None:
                    self.__description = I18n(self.__data.get("description", {}))
                return self.__description

            @property
            def ip(self) -> str:
                return self.__data.get("ip", "")

        def __init__(self, data: dict):
            self.__data = data

            self.__peripherals = None
            self.__middlewares = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def peripherals(self) -> dict[str, dict[str, ModuleUnit]]:
            if self.__peripherals is None:
                self.__peripherals = {}
                peripherals = self.__data.get("peripherals", {})
                for group_name, group in peripherals.items():
                    group_unit = {}
                    for name, unit in group.items():
                        group_unit[name] = Summary.Modules.ModuleUnit(
                            unit if unit is not None else {}
                        )
                    self.__peripherals[group_name] = group_unit
            return self.__peripherals

        @property
        def middlewares(self) -> dict[str, dict[str, ModuleUnit]]:
            if self.__middlewares is None:
                self.__middlewares = {}
                middlewares = self.__data.get("middlewares", {})
                for group_name, group in middlewares.items():
                    group_unit = {}
                    for name, unit in group.items():
                        group_unit[name] = Summary.Modules.ModuleUnit(
                            unit if unit is not None else {}
                        )
                    self.__middlewares[group_name] = group_unit
            return self.__middlewares

    class Linker:
        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def default_heap_size(self) -> int:
            size = self.__data.get("defaultHeapSize", -1)
            if isinstance(size, str):
                size = int(size, 16)
            return size

        @property
        def default_stack_size(self) -> int:
            size = self.__data.get("defaultStackSize", -1)
            if isinstance(size, str):
                size = int(size, 16)
            return size

    class Pin:
        def __init__(self, data: dict):
            self.__data = data
            self.__functions = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def position(self) -> int:
            return self.__data.get("position", -1)

        @property
        def type(self) -> str:
            return self.__data.get("type", "")

        @property
        def signals(self) -> list[str]:
            return self.__data.get("signals", [])

        @property
        def modes(self) -> list[str]:
            return self.__data.get("modes", [])

        # ----------------------------------------------------------------------

        def functions(self) -> list[str]:
            if self.__functions is None:
                self.__functions = self.signals + self.modes
            return self.__functions

    def __init__(self, data: dict):
        self.__data = data

        self.__vendor_url = None
        self.__documents = None
        self.__illustrate = None
        self.__introduction = None
        self.__modules = None
        self.__url = None
        self.__linker = None
        self.__pins = None

        # ----------------------------------------------------------------------

        self.__module_list = None
        self.__pin_instance = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @property
    def clock_tree(self) -> str:
        return self.__data.get("clockTree", "")

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @property
    def vendor_url(self) -> I18n:
        if self.__vendor_url is None:
            self.__vendor_url = I18n(self.__data.get("vendorUrl", {}))
        return self.__vendor_url

    @property
    def documents(self) -> Documents:
        if self.__documents is None:
            self.__documents = Summary.Documents(
                self.__data.get("documents", {})
            )
        return self.__documents

    @property
    def hals(self) -> list[str]:
        return self.__data.get("hals", [])

    @property
    def has_power_pad(self) -> bool:
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
            self.__modules = Summary.Modules(self.__data.get("modules", {}))
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
    def builder(self) -> dict[str, dict[str, list[str]]]:
        return self.__data.get("builder", {})

    @property
    def linker(self) -> Linker:
        if self.__linker is None:
            self.__linker = Summary.Linker(self.__data.get("linker", {}))
        return self.__linker

    @property
    def pins(self) -> dict[str, Pin]:
        if self.__pins is None:
            self.__pins = {}
            pins = self.__data.get("pins", {})
            for name, unit in pins.items():
                self.__pins[name] = Summary.Pin(
                    unit if unit is not None else {}
                )
        return self.__pins

    # ----------------------------------------------------------------------------------------------------------------------

    def module_list(self) -> dict[str, Modules]:
        if self.__module_list is None:
            self.__module_list = {}
            modules = self.modules
            for group_name, group in modules.peripherals.items():
                for name, module in group.items():
                    self.__module_list[name] = module
            for group_name, group in modules.middlewares.items():
                for name, module in group.items():
                    self.__module_list[name] = module
        return self.__module_list

    def pin_instance(self) -> str:
        if self.__pin_instance is None:
            for _, pin in self.pins.items():
                if len(pin.modes) > 0:
                    self.__pin_instance = pin.modes[0].split(":")[0]
                    break
        return self.__pin_instance or ""
