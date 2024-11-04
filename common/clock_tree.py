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

import os

import jsonschema
import yaml
from loguru import logger

from .settings import SETTINGS


class ClockTreeType:
    def __init__(self, clockTree: dict):
        pass


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

    @property
    def clockTrees(self) -> dict[str, ClockTreeType]:
        return self.__clockTrees
