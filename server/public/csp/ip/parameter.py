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
# @file        parameter.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#


import json

from ..i18n import I18n
from .parameter_value_unit import ParameterValueUnit


class Parameter:
    def __init__(self, data: dict):
        self.__data = data
        self.__display = None
        self.__description = None
        self.__values = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def display(self) -> I18n:
        if self.__display is None:
            self.__display = I18n(self.__data.get("display", {}))
        return self.__display

    @property
    def description(self) -> I18n:
        if self.__description is None:
            self.__description = I18n(self.__data.get("description", {}))
        return self.__description

    @property
    def readonly(self) -> bool:
        return self.__data.get("readonly", False)

    @property
    def type(self) -> str:
        return self.__data.get("type", "")

    @property
    def values(self) -> dict[str, ParameterValueUnit]:
        if self.__values is None:
            self.__values = {}
            values = self.__data.get("values", {})
            for name, unit in values.items():
                self.__values[name] = ParameterValueUnit(
                    unit if unit is not None else {}
                )
        return self.__values

    @property
    def group(self) -> str:
        return self.__data.get("group", "")

    @property
    def default(self) -> str | int | float | bool:
        return self.__data.get("default", "")

    @property
    def visible(self) -> bool:
        return self.__data.get("visible", True)

    @property
    def max(self) -> int | float | str:
        return self.__data.get("max", 2147483647)  # int32 最大值

    @property
    def min(self) -> int | float | str:
        return self.__data.get("min", -2147483648)  # int32 最小值
