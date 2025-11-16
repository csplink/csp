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
# @file        py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-09     xqyjlj       initial version
#

from __future__ import annotations

import json
from typing import Any

from .base_ref import BaseRef
from .base_ref_condition import BaseRefCondition
from .containers import Containers
from .parameter import Parameter
from .parameter_condition import ParameterCondition


class Ip:

    def __init__(self, data: dict):
        self.__data = data

        self.__parameters = None
        self.__containers = None
        self.__presets = None
        self.__pins = None
        self.__clockTree = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @property
    def parameters(
        self,
    ) -> dict[str, Parameter | list[ParameterCondition]]:
        if self.__parameters is None:
            self.__parameters = {}
            parameters = self.__data.get("parameters", {})
            for name, param in parameters.items():
                if isinstance(param, list):
                    self.__parameters[name] = [
                        ParameterCondition(item if item is not None else {})
                        for item in param
                    ]
                elif isinstance(param, dict):
                    self.__parameters[name] = Parameter(param)
                else:
                    self.__parameters[name] = Parameter({})
        return self.__parameters

    @property
    def containers(self) -> Containers:
        if self.__containers is None:
            self.__containers = Containers(self.__data.get("containers", {}))
        return self.__containers

    @property
    def presets(
        self,
    ) -> dict[str, BaseRef | list[BaseRefCondition]]:
        if self.__presets is None:
            self.__presets = {}
            presets = self.__data.get("presets", {})
            for name, preset in presets.items():
                if isinstance(preset, list):
                    self.__presets[name] = [
                        BaseRefCondition(item if item is not None else {})
                        for item in preset
                    ]
                elif isinstance(preset, dict):
                    self.__presets[name] = BaseRef(preset)
                else:
                    self.__presets[name] = BaseRef({})
        return self.__presets

    @property
    def pins(self) -> dict[str, dict[str, dict[str, dict[str, Any]]]]:
        if self.__pins is None:
            self.__pins = self.__data.get("pins", {})
        return self.__pins

    @property
    def clockTree(self) -> dict:
        if self.__clockTree is None:
            self.__clockTree = self.__data.get("clockTree", {})
        return self.__clockTree

    @property
    def activated(self) -> str:
        return self.__data.get("activated", "")
