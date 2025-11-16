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
# @file        module.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#


import json

from .module_unit import ModuleUnit


class Modules:

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
                    group_unit[name] = ModuleUnit(unit if unit is not None else {})
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
                    group_unit[name] = ModuleUnit(unit if unit is not None else {})
                self.__middlewares[group_name] = group_unit
        return self.__middlewares
