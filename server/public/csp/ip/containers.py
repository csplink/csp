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
# @file        containers.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-13     xqyjlj       initial version
#


import json

from .base_ref import BaseRef
from .base_ref_condition import BaseRefCondition


class Containers:
    def __init__(self, data: dict):
        self.__data = data
        self.__overview = None
        self.__modes = None
        self.__configurations = None
        self.__clockTree = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def overview(self) -> BaseRef | list[BaseRefCondition]:
        if self.__overview is None:
            overview = self.__data.get("overview")
            if isinstance(overview, list):
                self.__overview = [
                    BaseRefCondition(item if item is not None else {})
                    for item in overview
                ]
            elif isinstance(overview, dict):
                self.__overview = BaseRef(overview)
            else:
                self.__overview = BaseRef({})
        return self.__overview

    @property
    def modes(self) -> BaseRef | list[BaseRefCondition]:
        if self.__modes is None:
            modes = self.__data.get("modes")
            if isinstance(modes, list):
                self.__modes = [
                    BaseRefCondition(item if item is not None else {}) for item in modes
                ]
            elif isinstance(modes, dict):
                self.__modes = BaseRef(modes)
            else:
                self.__modes = BaseRef({})
        return self.__modes

    @property
    def configurations(self) -> BaseRef | list[BaseRefCondition]:
        if self.__configurations is None:
            configurations = self.__data.get("configurations")
            if isinstance(configurations, list):
                self.__configurations = [
                    BaseRefCondition(item if item is not None else {})
                    for item in configurations
                ]
            elif isinstance(configurations, dict):
                self.__configurations = BaseRef(configurations)
            else:
                self.__configurations = BaseRef({})
        return self.__configurations

    @property
    def clockTree(self) -> BaseRef | list[BaseRefCondition]:
        if self.__clockTree is None:
            clockTree = self.__data.get("clockTree")
            if isinstance(clockTree, list):
                self.__clockTree = [
                    BaseRefCondition(item if item is not None else {})
                    for item in clockTree
                ]
            elif isinstance(clockTree, dict):
                self.__clockTree = BaseRef(clockTree)
            else:
                self.__clockTree = BaseRef({})
        return self.__clockTree
