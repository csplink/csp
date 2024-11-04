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
# @file        ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-11-02     xqyjlj       initial version
#

import json
import os

import jsonschema
import yaml
from loguru import logger

from .settings import SETTINGS


class IpType:
    class ParameterUnitType:
        class ValueUnitType:
            def __init__(self, data: dict):
                self.__data = data

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def comment(self) -> dict[str, str]:
                return self.__data.get("comment", {})

        def __init__(self, data: dict):
            self.__data = data
            self.__values = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def type(self) -> str:
            return self.__data.get("type", '')

        @property
        def values(self) -> dict[str, ValueUnitType]:
            if self.__values is None:
                self.__values = {}
                for name, value in self.__data.get('values', {}).items():
                    self.__values[name] = self.ValueUnitType(value)
            return self.__values

        @property
        def displayName(self) -> dict[str, str]:
            return self.__data.get("displayName", {})

        @property
        def description(self) -> dict[str, str]:
            return self.__data.get("description", {})

        @property
        def default(self) -> str:
            return self.__data.get("default", '')

        @property
        def readonly(self) -> bool:
            return self.__data.get("readonly", True)

        @property
        def visible(self) -> bool:
            return self.__data.get("visible", True)

    class ModeUnitType:
        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def values(self) -> list[str]:
            return self.__data.get("values", [])

        @property
        def default(self) -> str:
            return self.__data.get("default", '')

    def __init__(self, data: dict):
        self.__data = data
        self.__parameters = None
        self.__modes = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def parameters(self) -> dict[str, ParameterUnitType]:
        if self.__parameters is None:
            self.__parameters = {}
            for name, param in self.__data.get("parameters", {}).items():
                self.__parameters[name] = IpType.ParameterUnitType(param)
        return self.__parameters

    @property
    def modes(self) -> dict[str, dict[str, ModeUnitType]]:
        if self.__modes is None:
            self.__modes = {}
            for name, modeItem in self.__data.get("modes", {}).items():
                self.__modes[name] = {}
                for modeName, mode in modeItem.items():
                    self.__modes[name][modeName] = IpType.ModeUnitType(mode)
        return self.__modes


class Ip:

    def __init__(self):
        self.__ips = {}

    @logger.catch(default=False)
    def __checkIp(self, ip: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "ip.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=ip, schema=schema)
        return True

    @logger.catch(default=IpType({}))
    def __getIp(self, vendor: str, name: str) -> IpType:
        file = os.path.join(SETTINGS.DATABASE_FOLDER, "ip", vendor.lower(), f"{name.lower()}.yml")
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as f:
                ip = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkIp(ip)
            if succeed:
                return IpType(ip)
            else:
                return IpType({})
        else:
            logger.error(f"{file} is not file!")
            return IpType({})

    def loadIp(self, vendor: str, instance: str, name: str):
        # noinspection PyTypeChecker,PyArgumentList
        ip = self.__getIp(vendor, name)
        if vendor not in self.__ips:
            self.__ips[vendor] = {}
        self.__ips[vendor][instance] = ip

    def getIp(self, vendor: str, instance: str) -> IpType:
        if vendor in self.__ips and instance in self.__ips[vendor]:
            return self.__ips[vendor][instance]
        else:
            return IpType({})

    @property
    def ips(self) -> dict[str, dict[str, IpType]]:
        return self.__ips


IP = Ip()
