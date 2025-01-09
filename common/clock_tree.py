#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        clock_tree.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-28     xqyjlj       initial version
#

import json
import os

import jsonschema
import yaml
from loguru import logger

from .i18n_type import I18nType
from .settings import SETTINGS


class ClockTreeType:
    class ElementUnitType:
        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def refParameter(self) -> str:
            return self.__data.get("refParameter", '')

        @property
        def type(self) -> str:
            return self.__data.get("type", '')

        @property
        def enable(self) -> str | bool | None:
            return self.__data.get("enable", None)

        @property
        def output(self) -> list[str]:
            return self.__data.get("output", [])

        @property
        def input(self) -> list[str]:
            return self.__data.get("input", [])

        @property
        def z(self) -> int:
            return self.__data.get("z", -1)

    def __init__(self, data: dict):
        self.__data = data
        self.__elements = None
        self.__i18n = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def elements(self) -> dict[str, ElementUnitType]:
        if self.__elements is None:
            self.__elements = {}
            for name, element in self.__data.get('elements', {}).items():
                self.__elements[name] = self.ElementUnitType(element)
        return self.__elements

    @property
    def i18n(self) -> dict[str, I18nType]:
        if self.__i18n is None:
            self.__i18n = {}
            for name, i in self.__data.get('i18n', {}).items():
                self.__i18n[name] = I18nType(i)
        return self.__i18n

    def i18nOrigin(self) -> dict[str, I18nType]:
        return self.__data.get('i18n', {})


class ClockTree:

    def __init__(self):
        self.__clockTrees = {}

    @logger.catch(default=False)
    def __checkClockTree(self, clockTree: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "clock_tree.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=clockTree, schema=schema)
        return True

    @logger.catch(default=ClockTreeType({}))
    def __getClockTree(self, vendor: str, name: str) -> ClockTreeType:
        file = os.path.join(SETTINGS.DATABASE_FOLDER, "clock", vendor.lower(), f"{name.lower()}.yml")
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as f:
                clockTree = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkClockTree(clockTree)
            if succeed:
                return ClockTreeType(clockTree)
            else:
                return ClockTreeType({})
        else:
            logger.error(f"{file} is not file!")
            return ClockTreeType({})

    def getClockTree(self, vendor: str, name: str) -> ClockTreeType:
        vendor = vendor.lower()
        name = name.lower()
        if vendor in self.__clockTrees and name in self.__clockTrees[vendor]:
            return self.__clockTrees[vendor][name]
        else:
            # noinspection PyTypeChecker,PyArgumentList
            clockTree = self.__getClockTree(vendor, name)
            if vendor not in self.__clockTrees:
                self.__clockTrees[vendor] = {}
            self.__clockTrees[vendor][name] = clockTree
            # noinspection PyTypeChecker
            return clockTree

    def clockTrees(self) -> dict[str, ClockTreeType]:
        return self.__clockTrees


CLOCK_TREE = ClockTree()
