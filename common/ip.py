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

        # ----------------------------------------------------------------------

        self.__total = None
        self.__total2 = None

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

    # ------------------------------------------------------------------------------------------------------------------

    def total(self) -> dict[str, str]:
        if self.__total is None:
            self.__total = {}
            locale = SETTINGS.get(SETTINGS.language).value.name()
            for _, parameter in self.parameters.items():
                for key, value in parameter.values.items():
                    self.__total[key] = value.comment[locale]
        return self.__total

    def total2(self) -> dict[str, str]:
        if self.__total2 is None:
            self.__total2 = {}
            locale = SETTINGS.get(SETTINGS.language).value.name()
            for _, parameter in self.parameters.items():
                for key, value in parameter.values.items():
                    self.__total2[value.comment[locale]] = key
        return self.__total2


class Ip:

    def __init__(self):
        self.__ips = {}

        # ----------------------------------------------------------------------
        self.__projectIps = {}

        self.__flushTotal = False
        self.__total = None
        self.__flushTotal2 = False
        self.__total2 = None

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

    def getIp(self, vendor: str, instance: str, name: str) -> IpType:
        if vendor in self.__ips and instance in self.__ips[vendor] and name in self.__ips[vendor][instance]:
            return self.__ips[vendor][instance][name]
        # noinspection PyTypeChecker,PyArgumentList
        ip = self.__getIp(vendor, name)
        if vendor not in self.__ips:
            self.__ips[vendor] = {}
        if instance not in self.__ips[vendor]:
            self.__ips[vendor][instance] = {}
        self.__ips[vendor][instance][name] = ip
        # noinspection PyTypeChecker
        return ip

    def ips(self) -> dict[str, dict[str, dict[str, IpType]]]:
        return self.__ips

    def setProjectIp(self, vendor: str, instance: str, name: str) -> IpType:
        self.__flushTotal = True
        self.__flushTotal2 = True
        ip = self.getIp(vendor, instance, name)
        self.__projectIps[instance] = ip
        return ip

    def projectIps(self) -> dict[str, IpType]:
        return self.__projectIps

    def total(self) -> dict[str, str]:
        if self.__total is None or self.__flushTotal:
            self.__total = {}
            self.__flushTotal = False
            for _, ip in self.projectIps().items():
                self.__total.update(ip.total())
        return self.__total

    def total2(self) -> dict[str, str]:
        if self.__total2 is None or self.__flushTotal2:
            self.__total2 = {}
            self.__flushTotal2 = False
            for _, ip in self.projectIps().items():
                self.__total2.update(ip.total2())
        return self.__total2

    def iptr(self, name: str) -> str:
        if name in self.total():
            return self.total()[name]
        else:
            return name

    def iptr2(self, name: str) -> str:
        if name in self.total2:
            return self.total2()[name]
        else:
            return name


IP = Ip()
