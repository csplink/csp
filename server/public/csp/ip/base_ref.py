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
# @file        base_ref.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-13     xqyjlj       initial version
#


import json

from .ref_parameter_unit import RefParameterUnit


class BaseRef:
    def __init__(self, data: dict):
        self.__data = data
        self.__refParameters = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def refParameters(self) -> dict[str, RefParameterUnit]:
        if self.__refParameters is None:
            self.__refParameters = {}
            refParameters = self.__data.get("refParameters", {})
            for name, unit in refParameters.items():
                self.__refParameters[name] = RefParameterUnit(
                    unit if unit is not None else {}
                )
        return self.__refParameters
