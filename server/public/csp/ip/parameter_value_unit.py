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
# @file        parameter_value_unit.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#


import json

from ..i18n import I18n
from .parameter_value_unit_signal_unit import ParameterValueUnitSignalUnit


class ParameterValueUnit:
    def __init__(self, data: dict):
        self.__data = data
        self.__comment = None
        self.__signals = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def comment(self) -> I18n:
        if self.__comment is None:
            self.__comment = I18n(self.__data.get("comment", {}))
        return self.__comment

    @property
    def signals(self) -> dict[str, ParameterValueUnitSignalUnit]:
        if self.__signals is None:
            self.__signals = {}
            signals = self.__data.get("signals", {})
            for name, unit in signals.items():
                self.__signals[name] = ParameterValueUnitSignalUnit(
                    unit if unit is not None else {}
                )
        return self.__signals
